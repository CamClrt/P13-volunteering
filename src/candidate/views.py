from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from candidate.forms import ActivityForm


@login_required
def dashboard(request):
    context = {
        "activities": request.user.candidateprofile.activity.all(),
    }
    return render(request, "candidate/dashboard.html", context)


@login_required
def activity(request):
    user = request.user.candidateprofile
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            user.activity.set(form.cleaned_data.get("name"))
        else:
            user.activity.clear()
        return redirect("candidate:dashboard")
    else:
        data = {}
        data["name"] = user.activity.all()
        form = ActivityForm(initial=data)
    return render(request, "candidate/activity.html", {"form": form})


@login_required
def wish(request):
    return render(request, "candidate/wish.html")


@login_required
def availability(request):
    return render(request, "candidate/availability.html")
