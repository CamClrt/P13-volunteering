from django.test import TestCase

from users.models import (  # isort:skip
    Address,
    CandidateProfile,
    City,
    CustomUser,
    OrganizationProfile,
    Sector,
)


class SectorModelTests(TestCase):
    def setUp(self):
        self.sector = Sector.objects.create(name="Fake sector")

    def test_sector_str(self):
        self.assertEqual(self.sector.__str__(), "Fake sector")

    def test_auto_slug(self):
        self.assertEqual(self.sector.slug, "fake-sector")


class CityModelTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Zion", zip_code="99999")

    def test_city_str(self):
        self.assertEqual(self.city.__str__(), "99999, ZION")


class AddressModelTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Zion", zip_code="99999")
        self.address = Address.objects.create(
            description="fake description",
            address_1="fake address 1",
            address_2="fake address 2",
            city=self.city,
        )

    def test_address_str(self):
        self.assertEqual(self.address.__str__(), "fake address 1, 99999, ZION")


class CustomUserModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="john.doe@mail.com",
            first_name="John",
            last_name="Doe",
            password="1234AZERTY$",
            status="BENEVOLE",
        )

    def test_custom_user_str(self):
        self.assertEqual(self.user.__str__(), "CustomUser: john.doe@mail.com")

    def test_has_perm(self):
        self.assertEqual(self.user.has_perm("fake permission"), True)

    def test_has_module_perms(self):
        self.assertEqual(self.user.has_module_perms("fake app_label"), True)

    def test_is_staff(self):
        self.assertEqual(self.user.is_staff, False)

    def test_simple_user_not_admin_str(self):
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
        self.sector = Sector.objects.create(name="Autres")
        self.user1 = CustomUser.objects.create_user(
            email="john.doe@mail.com",
            first_name="John",
            last_name="Doe",
            password="1234AZERTY$",
            status="ASSOCIATION",
        )

    def test_create_organization_profile_by_signal(self):
        self.assertEqual(OrganizationProfile.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(City.objects.count(), 1)


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
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(City.objects.count(), 1)
