from collections.abc import Iterable

from django.contrib.auth.models import Permission

from app_core.models import CustomUser
from common.tests.utils import random_char, random_email


def assign_permission(user: CustomUser, permission: str):
    user.user_permissions.add(Permission.objects.get(name=permission))


def create_user(
    email=None,
    password=None,
    is_superuser=False,
    permissions=None,
    **kwargs,
) -> CustomUser:
    if not email:
        email = random_email()
    if not password:
        password = random_char(12)

    user: CustomUser = CustomUser.objects.create_user(
        email=email,
        password=password,
        is_superuser=is_superuser,
        **kwargs,
    )

    if permissions is not None:
        if isinstance(permissions, str):
            assign_permission(user, permissions)
        elif isinstance(permissions, Iterable):
            for permission_name in permissions:
                assign_permission(user, permission_name)

    return user
