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
            Status.objects.create(name="Bénévole")
            Status.objects.create(name="Association")
        except IntegrityError:
            logging.warning("data already existed")
        logging.info("data insertion in DB: finished")
        return
