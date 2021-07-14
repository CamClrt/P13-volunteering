# Generated by Django 3.2.5 on 2021-07-13 15:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Activity",
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
                    "name",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("autres", "Autres"),
                            ("base-de-donnees", "Base de données"),
                            (
                                "developpement-back-end",
                                "Développement Back-end",
                            ),  # noqa: E501
                            (
                                "developpement-front-end",
                                "Développement Front-end",
                            ),  # noqa: E501
                            (
                                "developpement-full-stack",
                                "Développement Full-Stack",
                            ),  # noqa: E501
                            ("gestion-de-projet", "Gestion de projet"),
                            (
                                "gestion-de-site-reseaux-sociaux",
                                "Gestion de site & réseaux sociaux",
                            ),
                            ("marketing", "Marketing"),
                            ("produit", "Produit"),
                            ("pedagogie-formation", "Pédagogie & formation"),
                            ("seosea", "SEO/SEA"),
                            ("support", "Support"),
                            ("systeme", "Système"),
                        ],
                        max_length=50,
                        unique=True,
                    ),
                ),
            ],
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
                    "created_on",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),  # noqa: E501
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                ("hour_per_session", models.PositiveSmallIntegerField()),
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
                    ),
                ),
            ],
        ),
    ]