from django.test import TestCase
from django.urls import reverse


class TestHomeView(TestCase):
    def test_display_home_page(self):
        response = self.client.get(reverse("home:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/home.html")

    def test_display_legal_notices(self):
        response = self.client.get(reverse("home:legal_notices"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/legal_notices.html")
