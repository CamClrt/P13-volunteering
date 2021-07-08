from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import Address, CandidateProfile, City, OrganizationProfile

from .forms import (  # isort:skip
    AddressForm,
    CandidateProfileForm,
    CityForm,
    OrganizationProfileForm,
    UserForm,
    UserRegistrationForm,
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
    if request.method == "POST":
        user = request.user

        try:
            candidate = CandidateProfile.objects.get(user=user)
        except ObjectDoesNotExist:
            pass

        try:
            organization = OrganizationProfile.objects.get(user=user)
        except ObjectDoesNotExist:
            pass

        return HttpResponseRedirect(request.path)

    else:
        user = request.user

        try:
            candidate = CandidateProfile.objects.get(user=user)
            address = Address.objects.get(id=candidate.location.id)
            city = City.objects.get(id=address.city.id)

            if candidate:
                context = {
                    "profile": candidate,
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
            # sector = Sector.objects.get(id=organization.sector.id)
            address = Address.objects.get(id=organization.location.id)
            city = City.objects.get(id=address.city.id)

            if organization:
                context = {
                    "profile": organization,
                    "organization_profile_form": OrganizationProfileForm(
                        instance=organization,
                    ),
                    "city_form": CityForm(instance=city),
                    "address_form": AddressForm(instance=address),
                }
        except ObjectDoesNotExist:
            pass

        context["user_form"] = UserForm(instance=user)

        return render(request, "users/profile.html", context)
