from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView

from candidate.forms import ActivityForm, AvailabilityForm
from candidate.models import Availability


@method_decorator(login_required, name="dispatch")
class Dashboard(TemplateView):
    template_name = "candidate/dashboard.html"

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activities"] = request.user.candidateprofile.activity.all()
        context[
            "availabilities"
        ] = request.user.candidateprofile.availability.all()  # noqa: E501
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)


@method_decorator(login_required, name="dispatch")
class DisplayActivity(FormView):
    template_name = "candidate/activity.html"
    form_class = ActivityForm
    success_url = reverse_lazy("candidate:dashboard")

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        data = {}
        data["name"] = request.user.candidateprofile.activity.all()
        context["form"] = ActivityForm(initial=data)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            request.user.candidateprofile.activity.set(
                form.cleaned_data.get("name"),
            )
        else:
            request.user.candidateprofile.activity.clear()
        return self.form_valid(form)


@method_decorator(login_required, name="dispatch")
class DisplayAvailability(FormView):
    template_name = "candidate/availability.html"
    form_class = AvailabilityForm
    success_url = reverse_lazy("candidate:availability")

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "availabilities"
        ] = request.user.candidateprofile.availability.all()  # noqa: E501
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            availability = Availability.objects.create(
                type=data["type"],
                hour_per_session=data["hour_per_session"],
                start_date=data["start_date"],
                end_date=data["end_date"],
            )
            request.user.candidateprofile.availability.add(availability)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name="dispatch")
class RemoveAvailability(View):
    def get(self, request, availability_id, *args, **kwargs):
        availability = Availability.objects.get(pk=availability_id)
        request.user.candidateprofile.availability.remove(availability)
        return redirect("candidate:availability")


@login_required
def wish(request):
    return render(request, "candidate/wish.html")
