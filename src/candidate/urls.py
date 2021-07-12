from django.urls import path

from .views import activity, availability, dashboard, wish

app_name = "candidate"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("activity/", activity, name="activity"),
    path("availability/", availability, name="availability"),
    path("wish/", wish, name="wish"),
]
