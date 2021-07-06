from django.test import Client, TestCase
from django.urls import reverse

from users.models import CustomUser, Status


class TestRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_get(self):
        response = self.client.get(reverse("users:register"))
        self.assertTemplateUsed(response, "users/register.html")
        self.assertEqual(response.status_code, 200)


class TestProfileView(TestCase):
    def setUp(self):
        self.client = Client()
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
