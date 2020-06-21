from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseNotFound

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView

from server import settings
from .forms import SignupForm, ParticipantForm, TournamentForm, SponsorForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .models import Tournament, Participation, Encounter
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.username = user.email
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            context = {
                "color": "green",
                "redirect": "/",
                "message": "Please confirm your email to complete registration."
            }
            return render(request, 'message_and_redirect.html', context)
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        context = {
            "message": "Email confirmed successfully.",
            "color": "green",
            "redirect": "/"
        }
        return render(request, 'message_and_redirect.html', context)
    else:
        context = {
            "message": "Actvation link is invalid.",
            "color": "red",
            "redirect": "/"
        }
        return render(request, 'message_and_redirect.html', context)


class TournamentListView(ListView):
    model = Tournament
    paginate_by = 10

    def get_queryset(self):
        t = Tournament.objects.filter(time__gte=timezone.now()).order_by('time')

        name = self.request.GET.get('search', None)
        if name is not None:
            t = t.filter(name__icontains=name)

        return t

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TournamentListView, self).get_context_data()
        context["search"] = self.request.GET.get('search', '')
        return context


class TournamentDetailView(DetailView):
    model = Tournament

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deadline_exceeded'] = timezone.now() > context['tournament'].application_deadline
        if context['deadline_exceeded']:
            context['tournament'].create_encounters()

        context["is_creator"] = context['tournament'].creator == context['view'].request.user
        context["full"] = context['tournament'].max_participants == context['tournament'].participants.count()
        try:
            Participation.objects.get(user=context['view'].request.user, tournament=context['tournament'])
        except (Participation.DoesNotExist, TypeError):
            context["signed_up"] = False
        else:
            context["signed_up"] = True

        encounters = context["tournament"].encounters
        context["encounters"] = encounters.filter(agreed=False)
        context["finished"] = all(encounters.values_list("agreed", flat=True))
        participants = context["tournament"].participants.all()
        context["scoreboard"] = sorted(participants, key=lambda p: -p.points)

        return context


class Profile(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tournaments"] = Tournament.objects.filter(participants__user=context['user'])
        context["encounters"] = Encounter.objects.filter(
            Q(participant1__user=context["user"]) | Q(participant2__user=context["user"]), Q(agreed=False))

        return context


@login_required
def tournament_signup(request, pk):
    try:
        tournament = Tournament.objects.get(pk=pk)
    except Tournament.DoesNotExist:
        context = {
            "message": "Requested tournament doesn't exist.",
            "color": "red",
            "redirect": "/"
        }
        return render(request, 'message_and_redirect.html', context)

    t_url = reverse('tournament_details', kwargs={"pk": tournament.id})

    if timezone.now() > tournament.application_deadline:
        context = {
            "message": "Submission deadline passed.",
            "color": "red",
            "redirect": t_url
        }
        return render(request, 'message_and_redirect.html', context)

    try:
        Participation.objects.get(user=request.user, tournament_id=pk)
        context = {
            "message": "You've already signed up to this tournament.",
            "color": "green",
            "redirect": t_url
        }
        return render(request, 'message_and_redirect.html', context)
    except Participation.DoesNotExist:

        if tournament.participants.count() == tournament.max_participants:
            context = {
                "message": "Participants limit exceeded.",
                "color": "red",
                "redirect": t_url
            }
            return render(request, 'message_and_redirect.html', context)

        form = ParticipantForm(request.POST or None)
        form.initial["tournament"] = tournament
        form.initial["user"] = request.user

        if form.is_valid():
            form.save()
            context = {
                "message": "Now you're signed up for a competition!",
                "color": "green",
                "redirect": t_url
            }
            return render(request, 'message_and_redirect.html', context)

        context = {"form": form,
                   "tournament_id": tournament.id}
        return render(request, "tournaments/participant_form.html", context)


@login_required
def tournament_new(request):
    form = TournamentForm(request.POST or None)
    form.initial['creator'] = request.user
    form.creator = request.user

    if form.is_valid():
        tournament = form.save()
        t_url = reverse('tournament_details', kwargs={"pk": tournament.id})

        context = {
            "message": "Tournament created successfully!",
            "color": "green",
            "redirect": t_url
        }
        return render(request, 'message_and_redirect.html', context)

    min_date = timezone.now() + timedelta(days=1)
    context = {"form": form,
               "minDate": f"{min_date.year}-{min_date.month}-{min_date.day}",
               "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY
               }
    return render(request, "tournaments/tournament_new.html", context)


@login_required
def tournament_edit(request, id):
    try:
        tournament = Tournament.objects.get(id=id)
    except Tournament.DoesNotExist:
        context = {
            "message": "Tournament does not exist!",
            "color": "red",
            "redirect": "/"
        }
        return render(request, 'message_and_redirect.html', context)

    t_url = reverse('tournament_details', kwargs={"pk": tournament.id})

    if tournament.creator != request.user:
        context = {
            "message": "You're not allowed to access this page.",
            "color": "red",
            "redirect": t_url
        }
        return render(request, 'message_and_redirect.html', context)

    if request.method == "GET":
        form = TournamentForm(instance=tournament)

        min_date = tournament.application_deadline
        context = {"tournament": tournament,
                   "form": form,
                   "minDate": f"{min_date.year}-{min_date.month}-{min_date.day}",
                   "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY
                   }
        return render(request, 'tournaments/tournament_edit.html', context)

    elif request.method == "POST":
        form = TournamentForm(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            context = {
                "message": "Changes saved.",
                "color": "green",
                "redirect": t_url
            }
            return render(request, 'message_and_redirect.html', context)


@login_required
def tournament_add_sponsor(request, id):
    try:
        tournament = Tournament.objects.get(id=id)
    except Tournament.DoesNotExist:
        context = {
            "message": "Tournament does not exist!",
            "color": "red",
            "redirect": "/"
        }
        return render(request, 'message_and_redirect.html', context)

    t_url = reverse('tournament_details', kwargs={"pk": tournament.id})

    if tournament.creator != request.user:
        context = {
            "message": "You're not allowed to access this page.",
            "color": "red",
            "redirect": t_url
        }
        return render(request, 'message_and_redirect.html', context)

    if request.method == "GET":
        form = SponsorForm()
        form.initial['tournament'] = tournament
        return render(request, 'tournaments/add_sponsor.html', {"form": form})

    elif request.method == "POST":
        form = SponsorForm(request.POST, request.FILES)
        form.tournament = tournament
        if form.is_valid():
            form.save()
            context = {
                "message": "Sponsor added successfully.",
                "color": "green",
                "redirect": t_url
            }
            return render(request, 'message_and_redirect.html', context)

        return render(request, 'tournaments/add_sponsor.html', {"form": form})


class EncounterDetailView(DetailView):
    model = Encounter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['participant'] = self.request.user in (
            context['encounter'].participant1.user, context['encounter'].participant2.user)
        if context['encounter'].whoami(self.request.user) == 1:
            context['winner_set'] = context['encounter'].winner1 is not None
        elif context['encounter'].whoami(self.request.user) == 2:
            context['winner_set'] = context['encounter'].winner2 is not None

        return context


def encounter_set_winner(request, pk, winner):
    try:
        encounter = Encounter.objects.get(id=pk)
    except Encounter.DoesNotExist:
        context = {
            "message": "This encounter does not exist.",
            "color": "red",
            "redirect": "/"
        }
        return render(request, 'message_and_redirect.html', context)

    if encounter.set_winner(request.user, winner):
        context = {
            "message": "Your answer has been saved correctly.",
            "color": "green",
            "redirect": reverse("encounter", kwargs={"pk": pk})
        }
        return render(request, 'message_and_redirect.html', context)
    else:
        context = {
            "message": "Your answer is inconsistent with other player's answer. You must provide answers one more time.",
            "color": "red",
            "redirect": reverse("encounter", kwargs={"pk": pk})
        }
        return render(request, 'message_and_redirect.html', context)
