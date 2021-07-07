from django.contrib.auth.models import (  # isort:skip
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.utils import timezone

from config import settings


class Status(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Type d'utilisateur",
    )
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Sector(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class City(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    zip_code = models.CharField(
        max_length=5,
    )

    def __str__(self):
        return f"{self.zip_code}, {self.name}"

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)


class Address(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="address",
        related_query_name="address",
    )
    description = models.CharField(
        max_length=250,
        unique=True,
    )
    address_1 = models.CharField(
        max_length=250,
    )
    address_2 = models.CharField(
        max_length=250,
        blank=True,
    )

    def __str__(self):
        return f"{self.address_1}, {self.city}"


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
    status = models.ForeignKey(
        Status,
        default="1",
        on_delete=models.SET_NULL,
        null=True,
    )
    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        max_length=255,
    )

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
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
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name="organization_location",
        related_query_name="organization_location",
    )
    name = models.CharField(
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


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name="candidate_location",
        related_query_name="candidate_location",
    )
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


def post_profile_save_receiver(sender, instance, created, **kwargs):
    """Create a profil when a new user is registered"""
    if created:
        if instance.status.name == "Bénévole":
            CandidateProfile.objects.create(user=instance)
        if instance.status.name == "Association":
            OrganizationProfile.objects.create(user=instance)


post_save.connect(post_profile_save_receiver, sender=settings.AUTH_USER_MODEL)
