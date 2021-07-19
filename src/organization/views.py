from django.views.generic import DetailView, ListView

from users.models import CandidateProfile


class Dashboard(ListView):
    model = CandidateProfile
    template_name = "organization/dashboard.html"
    context_object_name = "candidates"


class CandidateDetail(DetailView):
    model = CandidateProfile
    template_name = "organization/details.html"
    context_object_name = "candidate"
