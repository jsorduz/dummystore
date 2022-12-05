import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_up = False
        seconds = 1

        while db_up is False:
            try:
                self.check(databases=["default"])
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(f"Database unavailable, waiting {seconds} second...")
                time.sleep(seconds)
            else:
                db_up = True

            if seconds < 300:
                seconds *= 2

        self.stdout.write(self.style.SUCCESS("Database available!"))
