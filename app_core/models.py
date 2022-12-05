from typing import List

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import BooleanField, EmailField
from django.utils.translation import gettext_lazy as _

from app_core.managers import CustomUserManager
from common.models import BaseModel


class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = EmailField(unique=True, help_text=_("email address"))
    is_staff = BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates that this user can access admin portal."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
