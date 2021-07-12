"""Feed DB with command line"""

import logging

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from candidate.models import Activity


class Command(BaseCommand):
    help = "Create activities in database"

    def handle(self, *args, **kwargs):
        logging.info("Create activities in database")
        try:
            for activity in Activity.ACTIVITY_CHOICES:
                Activity.objects.create(name=activity[0])
        except IntegrityError:
            logging.warning("activity data already existed")
        logging.info("activity data insertion in DB: finished")
        return
