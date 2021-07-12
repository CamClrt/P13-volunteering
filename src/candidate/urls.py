from django.urls import path

from .views import dashboard

app_name = "candidate"

urlpatterns = [
    path(
        "dashboard/",
        dashboard,
        name="dashboard",
    ),
]
