from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


class TestProfileView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="inconnu@mail.com",
            password="1234AZERTY",
            first_name="John",
            last_name="Doe",
            status="BENEVOLE",
        )

    def test_display_dashboard_ok(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("candidate:dashboard"))
        self.assertTemplateUsed(response, "candidate/dashboard.html")
        self.assertEqual(response.status_code, 200)

    def test_display_dashboard_not_ok(self):
        response = self.client.get(reverse("candidate:dashboard"))
        self.assertEqual(response.status_code, 302)
