from django.contrib.auth.models import (  # isort:skip
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from PIL import Image

from candidate.models import Activity
from config import settings


class Sector(models.Model):
    SECTOR_CHOICES = [
        ("ASH", "Action sociale, Santé, Humanitaire"),
        ("CL", "Culture et loisirs"),
        ("DD", "Défense des droits"),
        ("EFI", "Education, Formation, Insertion"),
        ("S", "Sports"),
        ("A", "Autres"),
    ]

    entitled = models.CharField(
        max_length=(5),
        unique=True,
        blank=True,
        choices=SECTOR_CHOICES,
    )


class Location(models.Model):
    address_1 = models.CharField(
        max_length=250,
        blank=True,
    )
    address_2 = models.CharField(
        max_length=250,
        blank=True,
    )

    city = models.CharField(
        max_length=50,
        blank=True,
    )
    zip_code = models.CharField(
        max_length=5,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.city = self.city.upper()
        super().save(*args, **kwargs)


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, status, password=None):
        """
        Creates and saves a User with the given email,
        first_name, last_name and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            status=status,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        first_name,
        last_name,
        status,
        password=None,
    ):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            status=status,
        )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        max_length=255,
    )

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    date_joined = models.DateTimeField(default=timezone.now)

    STATUS_CHOICES = [
        ("BENEVOLE", "Un bénévole"),
        ("ASSOCIATION", "Une association"),
    ]

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        blank=False,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "status",
    ]

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.upper()
        super().save(*args, **kwargs)


class OrganizationProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    sector = models.ForeignKey(
        Sector,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sector",
        related_query_name="sector",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name="organization_location",
        related_query_name="organization_location",
    )
    denomination = models.CharField(
        max_length=50,
        blank=True,
    )
    rna_code = models.CharField(
        max_length=10,
        blank=True,
    )
    siret_code = models.CharField(
        max_length=14,
        blank=True,
    )
    email = models.EmailField(
        blank=True,
    )
    web_site_url = models.URLField(
        blank=True,
    )
    phone_number = models.CharField(
        max_length=10,
        blank=True,
    )
    description = models.TextField(
        max_length=500,
        blank=True,
    )
    logo = models.ImageField(
        default="default.jpg",
        upload_to="organization",
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.logo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.logo.path)


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name="candidate_location",
        related_query_name="candidate_location",
    )
    activity = models.ManyToManyField(Activity)

    description = models.TextField(
        max_length=500,
        blank=True,
    )
    web_site_url = models.URLField(
        blank=True,
    )
    linkedin_url = models.URLField(
        blank=True,
    )
    github_url = models.URLField(
        blank=True,
    )
    gitlab_url = models.URLField(
        blank=True,
    )
    avatar = models.ImageField(
        default="default.jpg",
        upload_to="candidate",
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


def post_profile_save_receiver(sender, instance, created, **kwargs):
    """Create a profil and other infos, when user is registered"""
    if created:
        location = Location.objects.create(
            address_1="",
            address_2="",
            city="",
            zip_code="",
        )

        if instance.status == "BENEVOLE":
            CandidateProfile.objects.create(
                user=instance,
                location=location,
            )

        if instance.status == "ASSOCIATION":
            sector = Sector.objects.all()
            if not sector:
                sector = Sector.objects.create(entitled="A")
                sector = Sector.objects.create(entitled="ASH")
                sector = Sector.objects.create(entitled="CL")
                sector = Sector.objects.create(entitled="DD")
                sector = Sector.objects.create(entitled="EFI")
                sector = Sector.objects.create(entitled="S")

            OrganizationProfile.objects.create(
                user=instance,
                location=location,
                sector=Sector.objects.get(entitled="A"),
            )


post_save.connect(post_profile_save_receiver, sender=settings.AUTH_USER_MODEL)
