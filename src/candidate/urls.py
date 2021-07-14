from django.urls import path

from .views import (  # isort:skip
    Dashboard,
    DisplayAvailability,
    RemoveAvailability,
    activity,
    wish,
)

app_name = "candidate"

urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("activity/", activity, name="activity"),
    path("availability/", DisplayAvailability.as_view(), name="availability"),
    path(
        "availability/remove/<int:availability_id>",
        RemoveAvailability.as_view(),
        name="remove_availability",
    ),
    path("wish/", wish, name="wish"),
]
