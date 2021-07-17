# Generated by Django 3.2.5 on 2021-07-17 20:24

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("candidate", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),  # noqa: E501
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",  # noqa: E501
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="email"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=50, verbose_name="prénom"),
                ),  # noqa: E501
                (
                    "last_name",
                    models.CharField(max_length=50, verbose_name="nom"),
                ),  # noqa: E501
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("BENEVOLE", "Un bénévole"),
                            ("ASSOCIATION", "Une association"),
                        ],
                        max_length=25,
                        verbose_name="type de compte",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="actif"),
                ),  # noqa: E501
                (
                    "is_admin",
                    models.BooleanField(
                        default=False, verbose_name="administrateur"
                    ),  # noqa: E501
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",  # noqa: E501
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Availability",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("start_date", models.DateField(verbose_name="date de début")),
                (
                    "end_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="date de fin"
                    ),  # noqa: E501
                ),
                (
                    "hour_per_session",
                    models.PositiveSmallIntegerField(
                        verbose_name="nombre d'heures par session"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("ponctuel", "Ponctuel"),
                            ("journalier", "Chaque jour"),
                            ("hebdomadaire", "Chaque semaine"),
                            ("quinzomadaire", "Toutes les 2 semaines"),
                            ("mensuel", "Chaque mois"),
                            ("bimestriel", "Tous les 2 mois"),
                            ("trimestriel", "Chaque trimestre"),
                        ],
                        max_length=50,
                        verbose_name="récurrence",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CandidateProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, max_length=500, verbose_name="bio"
                    ),  # noqa: E501
                ),
                (
                    "web_site_url",
                    models.URLField(blank=True, verbose_name="site"),
                ),  # noqa: E501
                (
                    "linkedin_url",
                    models.URLField(blank=True, verbose_name="Linkedin"),
                ),  # noqa: E501
                (
                    "github_url",
                    models.URLField(blank=True, verbose_name="GitHub"),
                ),  # noqa: E501
                (
                    "gitlab_url",
                    models.URLField(blank=True, verbose_name="GitLab"),
                ),  # noqa: E501
                (
                    "avatar",
                    models.ImageField(
                        default="default.jpg",
                        upload_to="candidate",
                        verbose_name="avatar",
                    ),
                ),
                (
                    "activities",
                    models.ManyToManyField(
                        related_name="candidates_as_activity",
                        to="candidate.Activity",  # noqa: E501
                    ),
                ),
                (
                    "availabilities",
                    models.ManyToManyField(
                        related_name="candidates_as_availability",
                        to="users.Availability",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "address_1",
                    models.CharField(
                        blank=True, max_length=250, verbose_name="adresse"
                    ),
                ),
                (
                    "address_2",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        verbose_name="complément d'adresse",  # noqa: E501
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="ville"
                    ),  # noqa: E501
                ),
                (
                    "zip_code",
                    models.CharField(
                        blank=True, max_length=5, verbose_name="code postale"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Sector",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "entitled",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ASH", "Action sociale, Santé, Humanitaire"),
                            ("CL", "Culture et loisirs"),
                            ("DD", "Défense des droits"),
                            ("EFI", "Education, Formation, Insertion"),
                            ("S", "Sports"),
                            ("A", "Autres"),
                        ],
                        max_length=5,
                        unique=True,
                        verbose_name="intitulé",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Wish",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "remote",
                    models.BooleanField(
                        default=False, verbose_name="à distance"
                    ),  # noqa: E501
                ),
                (
                    "scoop",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("city", "Local"),
                            ("department", "Départemental"),
                            ("region", "Régional"),
                            ("country", "National"),
                        ],
                        max_length=20,
                        verbose_name="zone de déplacement",
                    ),
                ),
                (
                    "candidate",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.candidateprofile",
                    ),
                ),
                (
                    "sectors",
                    models.ManyToManyField(
                        related_name="wishes_as_sector", to="users.Sector"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OrganizationProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, max_length=500, verbose_name="bio"
                    ),  # noqa: E501
                ),
                (
                    "web_site_url",
                    models.URLField(blank=True, verbose_name="site"),
                ),  # noqa: E501
                ("denomination", models.CharField(blank=True, max_length=50)),
                (
                    "rna_code",
                    models.CharField(
                        blank=True, max_length=10, verbose_name="code RNA"
                    ),
                ),
                (
                    "siret_code",
                    models.CharField(
                        blank=True, max_length=14, verbose_name="code SIRET"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email"
                    ),  # noqa: E501
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True, max_length=10, verbose_name="téléphone"
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        default="default.jpg",
                        upload_to="organization",
                        verbose_name="logo",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.location",
                    ),
                ),
                (
                    "sector",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="organizationprofiles",
                        to="users.sector",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="candidateprofile",
            name="location",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.location",
            ),
        ),
        migrations.AddField(
            model_name="candidateprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,  # noqa: E501
            ),
        ),
    ]
