from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea

from .models import (  # isort:skip
    Address,
    CandidateProfile,
    City,
    CustomUser,
    OrganizationProfile,
    Sector,
)


class UserRegistrationForm(UserCreationForm):
    class Meta:

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
            "avatar",
            "web_site_url",
            "linkedin_url",
            "github_url",
            "gitlab_url",
            "description",
        ]
        labels = {
            "avatar": "",
            "web_site_url": "Site personnel",
            "linkedin_url": "Linkedin",
            "github_url": "GitHub",
            "gitlab_url": "GitLab",
            "description": "Bio",
        }
        widgets = {
            "web_site_url": Textarea(
                attrs={
                    "placeholder": "http(s)://www.votre-site.com",
                    "rows": "1",
                }
            ),
            "linkedin_url": Textarea(
                attrs={
                    "placeholder": "http(s)://www.votre-linkedin.com",
                    "rows": "1",
                }
            ),
            "github_url": Textarea(
                attrs={
                    "placeholder": "http(s)://www.votre-github.com",
                    "rows": "1",
                }
            ),
            "gitlab_url": Textarea(
                attrs={
                    "placeholder": "http(s)://www.votre-gitlab.com",
                    "rows": "1",
                }
            ),
        }


class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = [
            "logo",
            "denomination",
            "description",
            "rna_code",
            "siret_code",
            "email",
            "phone_number",
            "web_site_url",
        ]
        labels = {
            "logo": "",
            "denomination": "Dénomination de la structure",
            "description": "Description",
            "rna_code": "Code RNA",
            "siret_code": "SIRET",
            "email": "Mail de contact",
            "phone_number": "Téléphone",
            "web_site_url": "Site Web",
        }
        widgets = {
            "web_site_url": Textarea(
                attrs={
                    "placeholder": "http(s)://www.votre-site.com",
                    "rows": "1",
                }
            ),
            "rna_code": Textarea(
                attrs={
                    "placeholder": "W123456789",
                    "rows": "1",
                }
            ),
        }


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = [
            "name",
        ]
        labels = {
            "name": "Domaine d'activité",
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
