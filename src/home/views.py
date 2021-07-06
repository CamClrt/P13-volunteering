from django.shortcuts import render


def home(request):
    return render(request, "home/home.html")


def legal_notices(request):
    return render(request, "home/legal_notices.html")
