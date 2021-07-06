from django.test import TestCase

from users.models import CustomUser, Status


class StatusModelTests(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="Fake status")

    def test_status_str(self):
        self.assertEqual(self.status.__str__(), "Fake status")

    def test_auto_slug(self):
        self.assertEqual(self.status.slug, "fake-status")


class CustomUserModelTests(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="Fake status")
        self.user = CustomUser.objects.create_user(
            email="cam@mail.com",
            first_name="Cam",
            last_name="Clrt",
            password="1234AZERTY$",
            status=self.status,
        )

    def test_custom_user_str(self):
        self.assertEqual(self.user.__str__(), "cam@mail.com")

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
                status=self.status,
            )

    def test_superuser_is_admin_str(self):
        superuser = CustomUser.objects.create_superuser(
            first_name="Cam",
            last_name="Clrt",
            email="admin@gmail.com",
            password="1234AZERTY$",
            status=self.status,
        )
        self.assertIs(superuser.is_admin, True)
