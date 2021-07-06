"""Feed DB with command line"""

import logging

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from users.models import Sector

SECTOR = [
    "Action sociale, Santé, Humanitaire",
    "Culture et loisirs",
    "Défense des droits",
    "Education, Formation, Insertion",
    "Sports",
    "Autres",
]


class Command(BaseCommand):
    help = "Create user status in database"

    def handle(self, *args, **kwargs):
        logging.info("data insertion in DB: starting")
        try:
            for sector in SECTOR:
                Sector.objects.create(name=sector)
        except IntegrityError:
            logging.warning("sector data already existed")
        logging.info("sector data insertion in DB: finished")
        return
