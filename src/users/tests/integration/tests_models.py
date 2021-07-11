from django.test import TestCase

from users.models import (  # isort:skip
    Location,
    CandidateProfile,
    CustomUser,
    OrganizationProfile,
    Sector,
)


class LocationModelTests(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            address_1="fake address 1",
            address_2="fake address 2",
            city="zion",
            zip_code="99999",
        )

    def test_save_location(self):
        self.assertEqual(self.location.city, "ZION")


class CustomUserModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="john.doe@mail.com",
            first_name="John",
            last_name="Doe",
            password="1234AZERTY$",
            status="BENEVOLE",
        )

    def test_has_perm(self):
        self.assertEqual(self.user.has_perm("fake permission"), True)

    def test_has_module_perms(self):
        self.assertEqual(self.user.has_module_perms("fake app_label"), True)

    def test_is_staff(self):
        self.assertEqual(self.user.is_staff, False)

    def test_simple_user_not_admin(self):
        self.assertIs(self.user.is_admin, False)

    def test_create_simple_user_without_email(self):
        message = "Users must have an email address"
        with self.assertRaisesMessage(ValueError, message):
            CustomUser.objects.create_user(
                email="",
                first_name="Other",
                last_name="User",
                password="1234AZERTY$",
                status="BENEVOLE",
            )

    def test_superuser_is_admin_str(self):
        superuser = CustomUser.objects.create_superuser(
            first_name="Other",
            last_name="User",
            email="admin@gmail.com",
            password="1234AZERTY$",
            status="BENEVOLE",
        )
        self.assertIs(superuser.is_admin, True)


class OrganizationProfilModelTests(TestCase):
    def setUp(self):
        self.sector = Sector.objects.create(entitled="A")
        self.user1 = CustomUser.objects.create_user(
            email="john.doe@mail.com",
            first_name="John",
            last_name="Doe",
            password="1234AZERTY$",
            status="ASSOCIATION",
        )

    def test_create_organization_profile_by_signal(self):
        self.assertEqual(OrganizationProfile.objects.count(), 1)
        self.assertEqual(Location.objects.count(), 1)


class CandidateProfilModelTests(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            email="john.doe@mail.com",
            first_name="John",
            last_name="Doe",
            password="1234AZERTY$",
            status="BENEVOLE",
        )

    def test_create_candidate_profile_by_signal(self):
        self.assertEqual(CandidateProfile.objects.count(), 1)
        self.assertEqual(Location.objects.count(), 1)
