from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta:

        CHOICES = [
            ("1", "Un bénévole"),
            ("2", "Une association"),
        ]

        model = CustomUser
        fields = [
            "status",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        labels = {
            "status": "Vous êtes",
            "email": "Email",
            "first_name": "Prénom",
            "last_name": "Nom",
            "password1": "Mot de passe",
            "password2": "Confirmation du mot de passe",
        }
        widgets = {
            "status": forms.RadioSelect(choices=CHOICES),
        }
