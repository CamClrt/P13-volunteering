from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


class TestDashboardView(TestCase):
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


class TestActivityViews(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="inconnu@mail.com",
            password="1234AZERTY",
            first_name="John",
            last_name="Doe",
            status="BENEVOLE",
        )

    def test_display_activity_ok(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("candidate:activity"))
        self.assertTemplateUsed(response, "candidate/activity.html")
        self.assertEqual(response.status_code, 200)

    def test_display_activity_not_ok(self):
        response = self.client.get(reverse("candidate:activity"))
        self.assertEqual(response.status_code, 302)

    def test_display_availability_ok(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("candidate:availability"))
        self.assertTemplateUsed(response, "candidate/availability.html")
        self.assertEqual(response.status_code, 200)

    def test_display_availability_not_ok(self):
        response = self.client.get(reverse("candidate:availability"))
        self.assertEqual(response.status_code, 302)

    def test_display_wish_ok(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("candidate:wish"))
        self.assertTemplateUsed(response, "candidate/wish.html")
        self.assertEqual(response.status_code, 200)

    def test_display_wish_not_ok(self):
        response = self.client.get(reverse("candidate:wish"))
        self.assertEqual(response.status_code, 302)
