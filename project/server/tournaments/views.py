from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotModified, HttpResponseNotFound, \
    HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.views.generic import ListView, DetailView

from .forms import SignupForm, ParticipantForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .models import Tournament, Participation
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
            return HttpResponse('Please confirm your email address to complete the registration')
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
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


def home(request):
    return HttpResponse("Home")


class TournamentListView(ListView):
    model = Tournament
    paginate_by = 10

    def get_queryset(self):
        t = Tournament.objects.filter(time__gte=timezone.now()).order_by('time')

        name = self.request.GET.get('search', None)
        if name is not None:
            t = t.filter(name__icontains=name)

        return t


def tournament_details(request, id):
    return HttpResponse(str(id))


class TournamentDetailView(DetailView):
    model = Tournament

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deadline_exceeded'] = timezone.now() > context['tournament'].application_deadline
        context["is_creator"] = context['tournament'].creator == context['view'].request.user
        context["full"] = context['tournament'].max_participants == context['tournament'].participants.count()
        try:
            Participation.objects.get(user=context['view'].request.user, tournament=context['tournament'])
        except (Participation.DoesNotExist, TypeError):
            context["signed_up"] = False
        else:
            context["signed_up"] = True

        return context


class Profile(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required(login_url="/accounts/login")
def tournament_signup(request, pk):
    try:
        tournament = Tournament.objects.get(pk=pk)
    except Tournament.DoesNotExist:
        return HttpResponseNotFound("Requested tournament doesn't exist.")

    if timezone.now() > tournament.application_deadline:
        return HttpResponseForbidden("Submissions deadline passed")

    try:
        Participation.objects.get(user=request.user, tournament_id=pk)
        return HttpResponseNotModified()
    except Participation.DoesNotExist:
        if tournament.participants.count() == tournament.max_participants:
            return HttpResponseForbidden("Participants limit exceeded.")

        form = ParticipantForm(request.POST or None)

        if form.is_valid():
            p = Participation(user=request.user, tournament=tournament)
            p.ranking = form.cleaned_data["ranking"]
            p.license = form.cleaned_data["license"]
            p.save()
            return redirect('tournament_detail', tournament.id)

        context = {"form": form,
                   "tournament_id": tournament.id}
        return render(request, "tournaments/participant_form.html", context)
