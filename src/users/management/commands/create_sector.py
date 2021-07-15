"""Feed DB with command line"""

import logging

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from users.models import Sector


class Command(BaseCommand):
    help = "Create sector in database"

    def handle(self, *args, **kwargs):
        logging.info("data insertion in DB: starting")
        try:
            for sector in Sector.SECTOR_CHOICES:
                Sector.objects.create(entitled=sector[0])
        except IntegrityError:
            logging.warning("sector data already existed")
        logging.info("sector data insertion in DB: finished")
