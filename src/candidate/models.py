from django.db import models
from django.utils import timezone


class Activity(models.Model):
    ACTIVITY_CHOICES = [
        (
            "autres",
            "Autres",
        ),
        ("base-de-donnees", "Base de données"),
        ("developpement-back-end", "Développement Back-end"),
        ("developpement-front-end", "Développement Front-end"),
        ("developpement-full-stack", "Développement Full-Stack"),
        ("gestion-de-projet", "Gestion de projet"),
        (
            "gestion-de-site-reseaux-sociaux",
            "Gestion de site & réseaux sociaux",
        ),
        (
            "marketing",
            "Marketing",
        ),
        (
            "produit",
            "Produit",
        ),
        (
            "pedagogie-formation",
            "Pédagogie & formation",
        ),
        (
            "seosea",
            "SEO/SEA",
        ),
        (
            "support",
            "Support",
        ),
        (
            "systeme",
            "Système",
        ),
    ]

    name = models.CharField(
        max_length=(50),
        unique=True,
        blank=True,
        choices=ACTIVITY_CHOICES,
    )

    def __str__(self):
        for activity in self.ACTIVITY_CHOICES:
            if activity[0] == self.name:
                return activity[1]


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
