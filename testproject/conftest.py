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
def login_user() -> APIClient:
    """Login is required for requests"""
    client = APIClient()
    url = reverse("user-registration")
    response = client.post(
        url,
        data={
            "username": "test_user",
            "email": "test_user@at.com",
            "password": "test_user",
            "password2": "test_user",
            "first_name": "Test",
            "last_name": "User",
        },
        format="json",
    )
    token = response.json().get("access_token")
    client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token))
    return client


@pytest.fixture(scope="function", params=CURRENCY_CHOICES)
def create_wallet(request: Any, login_user: APIClient) -> Response:
    """
    Create Wallet instance
    """
    client = login_user
    url = reverse("wallet-list-create")
    response = client.post(
        url,
        data={"type": "visa", "currency": f"{request.param[0]}"},
        format="json",
    )

    return response
