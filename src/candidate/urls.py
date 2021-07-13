from django.urls import path

from .views import DisplayAvailability  # remove_availability,
from .views import RemoveAvailability, activity, dashboard, wish

app_name = "candidate"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("activity/", activity, name="activity"),
    path("availability/", DisplayAvailability.as_view(), name="availability"),
    path(
        "availability/remove/<int:availability_id>",
        RemoveAvailability.as_view(),
        name="remove_availability",
    ),
    path("wish/", wish, name="wish"),
]
