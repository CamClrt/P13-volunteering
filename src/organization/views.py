from django.views.generic import DetailView, ListView

from users.models import CustomUser


class Dashboard(ListView):
    queryset = CustomUser.objects.filter(status="BENEVOLE")
    template_name = "organization/dashboard.html"
    context_object_name = "users"
    paginate_by = 10


class CandidateDetail(DetailView):
    queryset = CustomUser.objects.filter(status="BENEVOLE")
    template_name = "organization/details.html"
    context_object_name = "user"
