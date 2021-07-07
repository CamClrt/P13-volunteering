from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import UserRegistrationForm


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
    return render(request, "users/profile.html")
