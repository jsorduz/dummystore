from django.test import TestCase
from rest_framework.test import APIClient

from app_core.tests.factory import create_user


class BasicViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.basic_user = create_user(email="basicuser@example.com")
        self.superuser = create_user(email="superuser@example.com", is_superuser=True)
        return super().setUp()
