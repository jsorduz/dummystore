import logging

from django.conf import settings
from django.core.management import BaseCommand

from app_core.models import CustomUser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not settings.SUPERUSER_EMAIL or not settings.SUPERUSER_PASSWORD:
            logger.error(
                "Not set initial superuser environment variables.",
            )
        elif CustomUser.objects.filter(is_superuser=True).count() == 0:
            logger.info("Creating initial superuser")
            CustomUser.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD,
            )
        else:
            logger.error(
                "Superuser can only be initialized if there is no other active superuser",
            )
