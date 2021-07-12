from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """Display the candidate dashboard"""
    return render(request, "candidate/dashboard.html")


@login_required
def activity(request):
    return render(request, "candidate/activity.html")


@login_required
def wish(request):
    return render(request, "candidate/wish.html")


@login_required
def availability(request):
    return render(request, "candidate/availability.html")
