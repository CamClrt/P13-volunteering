"""Feed DB with command line"""

import logging

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from users.models import Status


class Command(BaseCommand):
    help = "Create user status in database"

    def handle(self, *args, **kwargs):
        logging.info("data insertion in DB: starting")
        try:
            for status in ["Bénévole", "Association"]:
                Status.objects.create(name=status)
        except IntegrityError:
            logging.warning("status data already existed")
        logging.info("status data insertion in DB: finished")
        return
