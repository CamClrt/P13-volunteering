from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser, Status


class TestRegisterView(TestCase):
    def test_registration_get(self):
        response = self.client.get(reverse("users:register"))
        self.assertTemplateUsed(response, "users/register.html")
        self.assertEqual(response.status_code, 200)

    def test_registration_ok(self):
        data = {
            "status": "13",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@gmail.com",
            "password1": "1234AZERTY$",
            "password2": "1234AZERTY$",
        }

        Status.objects.create(name="Fake status")
        response = self.client.post(reverse("users:register"), data)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertRedirects(response, "/users/login/")

    def test_registration_fail(self):
        data = {
            "status": "12",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "1234AZERTY$",
            "password2": "1234AZERTY$",
        }

        Status.objects.create(name="Other Fake status")
        response = self.client.post(reverse("users:register"), data)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertEqual(response.status_code, 200)


class TestProfileView(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(
            email="john.doe@gmail.com",
            first_name="John",
            last_name="Doe",
            password="1234AZERTY",
            status=Status.objects.create(name="Fake status"),
        )

    def test_display_profile_ok(self):
        self.client.login(
            email="john.doe@gmail.com",
            password="1234AZERTY",
        )
        response = self.client.get(reverse("users:profile"))
        self.assertTemplateUsed(response, "users/profile.html")
        self.assertEqual(response.status_code, 200)

    def test_display_profile_not_ok(self):
        self.client.logout()
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 302)
