from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import CandidateProfile, OrganizationProfile

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

        if CandidateProfile.objects.filter(user=user.id).exists():
            pass

        if OrganizationProfile.objects.filter(user=user.id).exists():
            organization = request.user.organizationprofile

            organization_form = OrganizationProfileForm(
                request.POST, request.FILES, instance=organization
            )
            user_form = UserForm(request.POST, instance=user)
            city_form = CityForm(
                request.POST,
                instance=organization.location.city,
            )
            address_form = AddressForm(
                request.POST,
                instance=organization.location,
            )
            sector_form = SectorForm(
                request.POST,
                instance=organization.sector,
            )

            print(request.POST["name"])
            print(request.POST["entitled"])

            if sector_form.is_valid():
                sector_form.save()
            if user_form.is_valid():
                user_form.save()
            if city_form.is_valid():
                city_form.save()
            if address_form.is_valid():
                address_form.save()
            if organization_form.is_valid():
                organization_form.save()

        return HttpResponseRedirect(request.path)

    else:
        if CandidateProfile.objects.filter(user=user.id).exists():
            candidate = request.user.candidateprofile
            context = {
                "candidate_profile_form": CandidateProfileForm(
                    candidate=candidate,
                ),
                "city_form": CityForm(instance=candidate.location.city),
                "address_form": AddressForm(instance=candidate.location),
            }

        if OrganizationProfile.objects.filter(user=user.id).exists():
            organization = request.user.organizationprofile
            context = {
                "organization_profile_form": OrganizationProfileForm(
                    instance=organization
                ),
                "city_form": CityForm(instance=organization.location.city),
                "address_form": AddressForm(instance=organization.location),
                "sector_form": SectorForm(instance=organization.sector),
            }

        context["user_form"] = UserForm(instance=user)
        return render(request, "users/profile.html", context)
