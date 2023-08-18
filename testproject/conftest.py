"""
PyTest testing configurations, custom fixtures
"""

from typing import Any

import pytest
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient
from wallets.models import CURRENCY_CHOICES


@pytest.fixture(scope="function")
def login_user(request) -> tuple[APIClient, Response]:
    """
    Login is required for requests
    Output: Tuple, first element is instance of APIClient()
    second element is token of the user
    """
    client = APIClient()
    url = reverse("user-registration")
    data = {
        "username": "test_user",
        "email": "test_user@at.com",
        "password": "test_user",
        "password2": "test_user",
        "first_name": "Test",
        "last_name": "User",
    }
    response = client.post(
        url,
        data=data,
        format="json",
    )
    token = response.json().get("access_token")
    client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token))
    return client, token


@pytest.fixture(scope="function", params=CURRENCY_CHOICES)
def create_wallet(request: Any, login_user) -> Response:
    """
    Create Wallet instance
    """
    client = login_user[0]
    url = reverse("wallet-list-create")
    response = client.post(
        url,
        data={"type": "visa", "currency": f"{request.param[0]}"},
        format="json",
    )

    return response


@pytest.fixture(scope="function", params=CURRENCY_CHOICES)
def create_other_wallet(request: Any, login_user) -> Response:
    """
    Create Wallet instance
    """
    client = login_user[0]
    url = reverse("wallet-list-create")
    response = client.post(
        url,
        data={"type": "visa", "currency": f"{request.param[::-1][0]}"},
        format="json",
    )

    return response
