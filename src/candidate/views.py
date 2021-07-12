from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """Display the candidate dashboard"""
    return render(request, "candidate/dashboard.html")
