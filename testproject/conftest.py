import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture(scope="function")
def login_user():
    """Login is required for requests"""
    client = APIClient()
    url = reverse("user-registration")
    response = client.post(
        url,
        data={
            "username": "test_user",
            "email": "test_user@at.com",
            "password": "test_user",
            "first_name": "Test",
            "last_name": "User",
        },
        format="json",
    )
    token = response.json().get("access_token")
    client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token))
    return client


@pytest.fixture(scope="function")
def walletA(client):
    """
    Create Wallet instance
    """
    client = APIClient()
    url = reverse("wallet-list-create")
    response = client.post(url, data={}, format="json")
