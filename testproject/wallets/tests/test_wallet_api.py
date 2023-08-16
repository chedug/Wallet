"""
Testing wallets app
"""


import pytest
from conftest import login_user
from django.urls import reverse
from rest_framework import status
from wallets.models import Wallet

# Create your tests here


@pytest.mark.django_db
def test_create_wallet(login_user):
    """
    Test that wallet is created
    """
    client = login_user
    url = reverse("wallet-list-create")
    data = {"type": "visa", "currency": "GBP"}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_max_wallets(login_user):
    """
    Test that user cannot have too many wallets
    """
    client = login_user
    url = reverse("wallet-list-create")
    data = {"type": "visa", "currency": "GBP"}
    for i in range(Wallet.MAX_NUMBER_OF_WALLETS):
        # creating first MAX_NUMBER_OF_WALLETS should be ok
        response = client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
    response = client.post(
        url, data=data, format="json"
    )  # the last one should not be created
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_wallet_bonus(login_user):
    """
    Make sure that the appropriate bonus is added
    """
    pass
