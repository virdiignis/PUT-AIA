from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from tournaments.models import Participation, Tournament, Sponsor


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class ParticipantForm(ModelForm):
    class Meta:
        model = Participation
        fields = "__all__"


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'time': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'class': 'form-control datetimefield'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'place'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '1'}),
            'application_deadline': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                                        attrs={'class': 'form-control datetimefield'}),
        }


class SponsorForm(ModelForm):
    class Meta:
        model = Sponsor
        fields = "__all__"
        widgets = {
            'tournament': forms.HiddenInput()
        }
