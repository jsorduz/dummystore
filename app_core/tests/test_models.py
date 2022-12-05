import pytest

from app_core.models import CustomUser


# pylint: disable=E1120
@pytest.mark.django_db
def test_create_user():
    user = CustomUser.objects.create_user(
        email="basicuser@example.com", password="s3cret"
    )

    assert str(user) == "basicuser@example.com", "User __str___ should returns email"
    assert (
        user.email == "basicuser@example.com"
    ), "User should be created with given email"
    assert user.is_staff is False, "Basic user is not staff"
    assert user.is_staff is False, "Basic user is not superuser"


@pytest.mark.django_db
def test_create_user_wrong_fields():
    with pytest.raises(TypeError):
        CustomUser.objects.create_user()
    with pytest.raises(TypeError):
        CustomUser.objects.create_user(email="")
    with pytest.raises(ValueError):
        CustomUser.objects.create_user(email="", password="s3cret")


@pytest.mark.django_db
def test_create_superuser():
    superuser = CustomUser.objects.create_superuser(
        email="superuser@example.com", password="s3cret"
    )

    assert (
        superuser.email == "superuser@example.com"
    ), "User should be created with given email"
    assert superuser.is_staff is True, "Superser should be staff"
    assert superuser.is_staff is True, "Superser should be superuser"


@pytest.mark.django_db
def test_create_superuser_wrong_fields():
    with pytest.raises(TypeError):
        CustomUser.objects.create_superuser()
    with pytest.raises(TypeError):
        CustomUser.objects.create_superuser(email="")
    with pytest.raises(ValueError):
        CustomUser.objects.create_superuser(
            email="superuser@example.com", password="s3cret", is_superuser=False
        )
    with pytest.raises(ValueError):
        CustomUser.objects.create_superuser(
            email="superuser@example.com",
            password="s3cret",
            is_superuser=True,
            is_staff=False,
        )


# pylint: enable=E1120
