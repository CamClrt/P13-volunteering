from django.urls import path

from home.views import home, legal_notices

app_name = "home"

urlpatterns = [
    path("", home, name="home"),
    path("legal_notices", legal_notices, name="legal_notices"),
]
