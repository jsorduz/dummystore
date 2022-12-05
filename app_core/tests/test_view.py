import json

import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from app_core.models import CustomUser
from app_core.tests.factory import create_user

EXPECTED_USER_KEYS = {
    "id",
    "email",
    "created_at",
    "updated_at",
}
NON_EXPECTED_USER_KEYS = {
    "password",
}


def check_user_response(obtained_keys):
    if not isinstance(obtained_keys, set):
        obtained_keys = set(obtained_keys)
    assert (
        obtained_keys == EXPECTED_USER_KEYS
    ), f"Expected keys: {EXPECTED_USER_KEYS}, obtained_keys: {obtained_keys}"
    assert (
        NON_EXPECTED_USER_KEYS.intersection(obtained_keys) == set()
    ), f"Non expected keys: {NON_EXPECTED_USER_KEYS}, obtained_keys: {obtained_keys}"


@pytest.mark.django_db
def test_create_access_token():
    expected_access_token_response = {"access", "refresh", "token_type", "expires_in"}
    email = "user@example.com"
    password = "password"
    create_user(email, password)

    client: APIClient = APIClient()
    response = client.post(
        reverse("create-access-jwt-token"), data={"email": email, "password": password}
    )
    response_json = json.loads(response.content)
    obtained_keys = set(response_json.keys())

    assert (
        response.status_code == 200
    ), f"Expected 200 response, received {response.status_code}"
    assert (
        expected_access_token_response == obtained_keys
    ), f"Expected keys: {expected_access_token_response}, obtained_keys: {obtained_keys}"


@pytest.mark.django_db
def test_refresh_token():
    email = "user@example.com"
    password = "password"
    create_user(email, password)

    client: APIClient = APIClient()
    refresh_token = json.loads(
        client.post(
            reverse("create-access-jwt-token"),
            data={"email": email, "password": password},
        ).content
    )["refresh"]

    response = client.post(
        reverse("refresh-jwt-token"), data={"refresh": refresh_token}
    )
    response_json = json.loads(response.content)

    assert (
        response.status_code == 200
    ), f"Expected 200 response, received {response.status_code}"
    assert "access" in response_json.keys()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_data",
    [
        {
            "user": {"email": "basicuser@example.com"},
            "expected_status_code": 403,
        },
        {
            "user": {
                "email": "userwithpermission@example.com",
                "permissions": "Can view custom user",
            },
            "expected_status_code": 200,
        },
        {
            "user": {"email": "superuser@example.com", "is_superuser": True},
            "expected_status_code": 200,
        },
    ],
)
def test_list_users(user_data):
    user = create_user(**user_data["user"])
    create_user(email="existinguser1@example.com")
    create_user(email="existinguser2@example.com")
    client: APIClient = APIClient()
    client.force_authenticate(user)
    current_users = CustomUser.objects.all().count()

    response = client.get(reverse("user-list"))

    assert (
        response.status_code == user_data["expected_status_code"]
    ), f"Expected {user_data['expected_status_code']} response, received {response.status_code}"
    if user_data["expected_status_code"] == 200:
        obtained_results = json.loads(response.content)["results"]
        assert (
            len(obtained_results) == current_users
        ), f"Expected {user_data['expected_results']} results, obtained {len(obtained_results)} results"
        for obtained_result in obtained_results:
            check_user_response(obtained_result.keys())


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_data",
    [
        {
            "user": {"email": "basicuser@example.com"},
            "expected_status_code": 403,
        },
        {
            "user": {
                "email": "userwithpermission@example.com",
                "permissions": ("Can view custom user", "Can add custom user"),
            },
            "expected_status_code": 201,
        },
        {
            "user": {"email": "superuser@example.com", "is_superuser": True},
            "expected_status_code": 201,
        },
    ],
)
def test_create_user(user_data):
    user = create_user(**user_data["user"])
    email = "newuser@example.com"
    password = "password"
    client: APIClient = APIClient()
    client.force_authenticate(user)

    response = client.post(
        reverse("user-list"), data={"email": email, "password": password}
    )

    assert (
        response.status_code == user_data["expected_status_code"]
    ), f"Expected {user_data['expected_status_code']} response, received {response.status_code}"
    if user_data["expected_status_code"] == 201:
        assert CustomUser.objects.filter(
            email=email
        ).exists(), "Created user should be in db"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_data",
    [
        {
            "user": {"email": "basicuser@example.com"},
            "expected_status_code": 403,
        },
        {
            "user": {
                "email": "userwithpermission@example.com",
                "permissions": "Can view custom user",
            },
            "expected_status_code": 200,
        },
        {
            "user": {"email": "superuser@example.com", "is_superuser": True},
            "expected_status_code": 200,
        },
    ],
)
def test_retrieve_user(user_data):
    user = create_user(**user_data["user"])
    existing_user = create_user(email="user1@example.com")
    client: APIClient = APIClient()
    client.force_authenticate(user)

    response = client.get(reverse("user-detail", kwargs={"pk": existing_user.pk}))

    assert (
        response.status_code == user_data["expected_status_code"]
    ), f"Expected {user_data['expected_status_code']} response, received {response.status_code}"
    if user_data["expected_status_code"] == 200:
        obtained_result = json.loads(response.content)
        check_user_response(obtained_result.keys())


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_data",
    [
        {
            "user": {"email": "basicuser@example.com"},
            "expected_status_code": 403,
        },
        {
            "user": {
                "email": "userwithpermission@example.com",
                "permissions": "Can change custom user",
            },
            "expected_status_code": 200,
        },
        {
            "user": {"email": "superuser@example.com", "is_superuser": True},
            "expected_status_code": 200,
        },
    ],
)
def test_update_user(user_data):
    user = create_user(**user_data["user"])
    original_email = "user1@example.com"
    updated_email = "updatedemail@example.com"
    existing_user = create_user(email="user1@example.com")
    client: APIClient = APIClient()
    client.force_authenticate(user)

    response = client.patch(
        reverse("user-detail", kwargs={"pk": existing_user.pk}),
        data={"email": updated_email},
    )

    assert (
        response.status_code == user_data["expected_status_code"]
    ), f"Expected {user_data['expected_status_code']} response, received {response.status_code}"
    if user_data["expected_status_code"] == 200:
        obtained_result = json.loads(response.content)
        check_user_response(obtained_result.keys())
        assert not CustomUser.objects.filter(
            email=original_email
        ).exists(), f"Shouldn't exists an user with email = {original_email} in db"
        assert CustomUser.objects.filter(
            email=updated_email
        ).exists(), f"Should exists an user with email = {updated_email} in db"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_data",
    [
        {
            "user": {"email": "basicuser@example.com"},
            "expected_status_code": 403,
        },
        {
            "user": {
                "email": "userwithpermission@example.com",
                "permissions": "Can delete custom user",
            },
            "expected_status_code": 204,
        },
        {
            "user": {"email": "superuser@example.com", "is_superuser": True},
            "expected_status_code": 204,
        },
    ],
)
def test_delete_user(user_data):
    user = create_user(**user_data["user"])
    existing_user = create_user(email="user1@example.com")
    client: APIClient = APIClient()
    client.force_authenticate(user)

    response = client.delete(reverse("user-detail", kwargs={"pk": existing_user.pk}))

    assert (
        response.status_code == user_data["expected_status_code"]
    ), f"Expected {user_data['expected_status_code']} response, received {response.status_code}"
    if user_data["expected_status_code"] == 204:
        assert not CustomUser.objects.filter(
            email=existing_user.email
        ).exists(), f"Shouldn't exists an user with email = {existing_user.email} in db"


@pytest.mark.django_db
def test_get_me():
    create_user(email="existinguser1@example.com")
    create_user(email="existinguser2@example.com")
    user = create_user(email="user@example.com")
    client: APIClient = APIClient()
    client.force_authenticate(user)

    response = client.get(reverse("user-me"))

    assert (
        response.status_code == 200
    ), f"Expected 200 response, received {response.status_code}"
    obtained_result = json.loads(response.content)
    check_user_response(obtained_result.keys())


@pytest.mark.django_db
def test_endpoint_unauthenticated_user():
    user = create_user()
    create_user()
    client: APIClient = APIClient()

    for method, url in (
        ("get", reverse("user-list")),
        ("get", reverse("user-detail", kwargs={"pk": user.pk})),
        ("get", reverse("user-me")),
        ("post", reverse("user-list")),
        ("put", reverse("user-detail", kwargs={"pk": user.pk})),
        ("patch", reverse("user-detail", kwargs={"pk": user.pk})),
        ("delete", reverse("user-detail", kwargs={"pk": user.pk})),
    ):
        request = getattr(client, method)
        response = request(url)
        assert (
            response.status_code == 401
        ), f"Expected 401 response, received {response.status_code}"
