from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import (  # isort:skip
    Address,
    CandidateProfile,
    City,
    CustomUser,
    OrganizationProfile,
)


class UserRegistrationForm(UserCreationForm):
    class Meta:

        STATUS = [
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
            "status": forms.RadioSelect(choices=STATUS),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "last_name",
            "first_name",
        ]
        labels = {
            "first_name": "Votre prénom",
            "last_name": "Votre nom",
        }


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = [
            "web_site_url",
            "linkedin_url",
            "github_url",
            "gitlab_url",
            "description",
        ]
        labels = {
            "web_site_url": "Site personnel",
            "linkedin_url": "Linkedin",
            "github_url": "GitHub",
            "gitlab_url": "GitLab",
            "description": "Bio",
        }


class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = [
            "name",
            "sector",
            "description",
            "rna_code",
            "siret_code",
            "email",
            "phone_number",
            "web_site_url",
        ]
        labels = {
            "name": "Dénomination de la structure",
            "sector": "Secteur d'activité",
            "description": "Description",
            "rna_code": "Code RNA",
            "siret_code": "SIRET",
            "email": "Mail de contact",
            "phone_number": "Téléphone",
            "web_site_url": "Site Web",
        }
        widgets = {
            "sector": forms.RadioSelect(),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "address_1",
            "address_2",
        ]
        labels = {
            "address_1": "Adresse",
            "address_2": "Complément d'adresse",
        }


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = [
            "name",
            "zip_code",
        ]
        labels = {
            "name": "Ville",
            "zip_code": "Code postale",
        }
