from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import (  # isort:skip
    Address,
    CandidateProfile,
    City,
    OrganizationProfile,
    Sector,
)

from .forms import (  # isort:skip
    AddressForm,
    CandidateProfileForm,
    CityForm,
    OrganizationProfileForm,
    UserForm,
    UserRegistrationForm,
    SectorForm,
)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):

    user = request.user

    if request.method == "POST":

        try:
            candidate = CandidateProfile.objects.get(user=user)
            address = Address.objects.get(id=candidate.location.id)
            city = City.objects.get(id=address.city.id)

            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.save()

            candidate.web_site_url = request.POST["web_site_url"]
            candidate.linkedin_url = request.POST["linkedin_url"]
            candidate.github_url = request.POST["github_url"]
            candidate.gitlab_url = request.POST["gitlab_url"]
            candidate.description = request.POST["description"]
            candidate.save()

            try:
                city.name = request.POST["name"].upper()
                city.zip_code = request.POST["zip_code"]
                city.save()
            except IntegrityError:
                city = City.objects.filter(
                    name__exact=request.POST["name"].upper()
                ).first()
                address.city = city

            address.address_1 = request.POST["address_1"]
            address.address_2 = request.POST["address_2"]
            address.save()

        except ObjectDoesNotExist:
            pass

        try:
            organization = OrganizationProfile.objects.get(user=user)
            address = Address.objects.get(id=organization.location.id)
            city = City.objects.get(id=address.city.id)

            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.save()

            organization.rna_code = request.POST["rna_code"].upper()
            organization.siret_code = request.POST["siret_code"]
            organization.email = request.POST["email"]
            organization.phone_number = request.POST["phone_number"]
            organization.web_site_url = request.POST["web_site_url"]
            organization.denomination = request.POST["denomination"]
            organization.description = request.POST["description"]
            organization.sector = Sector.objects.get(id=request.POST["sector"])
            organization.save()

            address.address_1 = request.POST["address_1"]
            address.address_2 = request.POST["address_2"]
            address.save()

            try:
                city.name = request.POST["name"].upper()
                city.zip_code = request.POST["zip_code"]
                city.save()
            except IntegrityError:
                city = City.objects.filter(
                    name__exact=request.POST["name"].upper()
                ).first()
                address.city = city

            address.address_1 = request.POST["address_1"]
            address.address_2 = request.POST["address_2"]
            address.save()

        except ObjectDoesNotExist:
            pass

        return HttpResponseRedirect(request.path)

    else:
        try:
            candidate = CandidateProfile.objects.get(user=user)
            address = Address.objects.get(id=candidate.location.id)
            city = City.objects.get(id=address.city.id)

            if candidate:
                context = {
                    "candidate_profile_form": CandidateProfileForm(
                        instance=candidate,
                    ),
                    "city_form": CityForm(instance=city),
                    "address_form": AddressForm(instance=address),
                }
        except ObjectDoesNotExist:
            pass

        try:
            organization = OrganizationProfile.objects.get(user=user)
            sector = Sector.objects.get(id=organization.sector.id)
            address = Address.objects.get(id=organization.location.id)
            city = City.objects.get(id=address.city.id)

            if organization:
                context = {
                    "organization_profile_form": OrganizationProfileForm(
                        instance=organization,
                    ),
                    "city_form": CityForm(instance=city),
                    "address_form": AddressForm(instance=address),
                    "sector_form": SectorForm(instance=sector),
                }
        except ObjectDoesNotExist:
            pass

        context["user_form"] = UserForm(instance=user)

        return render(request, "users/profile.html", context)
