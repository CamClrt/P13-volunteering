from django.contrib.auth.models import (  # isort:skip
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from PIL import Image

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

    def __str__(self):
        return self.entitled


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

    def __str__(self):
        return f"{self.address_1}, {self.zip_code} {self.city}"

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

    def __str__(self):
        return self.email

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
        "users.Sector",
        on_delete=models.SET_NULL,
        null=True,
        related_name="sector",
        related_query_name="sector",
    )
    location = models.ForeignKey(
        "users.Location",
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

    def __str__(self):
        return f"{self.user}: {self.denomination}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.logo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.logo.path)


class Availability(models.Model):
    AVAILABILITY_CHOICES = [
        (
            "ponctuel",
            "Ponctuel",
        ),
        (
            "journalier",
            "Chaque jour",
        ),
        (
            "hebdomadaire",
            "Chaque semaine",
        ),
        (
            "quinzomadaire",
            "Toutes les 2 semaines",
        ),
        (
            "mensuel",
            "Chaque mois",
        ),
        (
            "bimestriel",
            "Tous les 2 mois",
        ),
        (
            "trimestriel",
            "Chaque trimestre",
        ),
    ]
    created_on = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    hour_per_session = models.PositiveSmallIntegerField()
    type = models.CharField(
        max_length=(50),
        choices=AVAILABILITY_CHOICES,
    )

    def __str__(self):
        return f"{self.id}: {self.type}, {self.hour_per_session}h"


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        "users.Location",
        on_delete=models.SET_NULL,
        null=True,
        related_name="candidate_location",
        related_query_name="candidate_location",
    )

    activity = models.ManyToManyField("candidate.Activity")
    availability = models.ManyToManyField("users.Availability")

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

    def __str__(self):
        return self.user

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


class Wish(models.Model):
    MOVE_CHOICES = [
        (
            "city",
            "Local",
        ),
        (
            "department",
            "Départemental",
        ),
        (
            "region",
            "Régional",
        ),
        (
            "country",
            "National",
        ),
    ]

    candidate = models.OneToOneField(
        "users.CandidateProfile",
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    remote = models.BooleanField(default=False)
    scoop = models.CharField(
        max_length=(20),
        blank=True,
        choices=MOVE_CHOICES,
    )
    sector = models.ManyToManyField("users.Sector")

    def __str__(self):
        return f"{self.candidate}: {self.remote}, {self.scoop}, {self.sector}"


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
            OrganizationProfile.objects.create(
                user=instance,
                location=location,
                sector=Sector.objects.get(entitled="A"),
            )


post_save.connect(post_profile_save_receiver, sender=settings.AUTH_USER_MODEL)
