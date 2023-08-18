"""
Tests for transactions app
"""
from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from transactions.models import Transaction


@pytest.mark.django_db
def test_create_transaction(login_user, create_wallet, create_other_wallet) -> None:
    """
    Test transactions between wallets of the same user
    """
    client = login_user[0]
    url = reverse("transaction-list")
    sender_wallet_name = create_wallet.data["name"]
    sender_currency = create_wallet.data["currency"]
    receiver_wallet_name = create_other_wallet.data["name"]
    receiver_currency = create_other_wallet.data["currency"]
    response = client.post(
        url,
        data={
            "sender": sender_wallet_name,
            "receiver": receiver_wallet_name,
            "transfer_amount": Decimal("1"),
        },
        format="json",
    )
    if sender_currency == receiver_currency:
        assert response.data["status"] == "PAID"
    if sender_currency != receiver_currency:
        # if currencies do not match validation error will raise bad request
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_different_owners(login_user, create_wallet):
    """
    check that commission is correct
    """
    client = login_user[0]
    token = login_user[1]
    sender_wallet = create_wallet
    wallet_currency = sender_wallet.data["currency"]

    client = APIClient()
    url = reverse("user-registration")
    data = {
        "username": "test_user2",
        "email": "test_user2@at.com",
        "password": "test_user2",
        "password2": "test_user2",
        "first_name": "Test2",
        "last_name": "User2",
    }
    response = client.post(
        url,
        data=data,
        format="json",
    )
    token = response.json().get("access_token")
    client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token))
    url = reverse("wallet-list-create")
    receiver_wallet = client.post(
        url,
        data={"type": "visa", "currency": f"{wallet_currency}"},
        format="json",
    )

    url = reverse("transaction-list")
    response = client.post(
        url,
        data={
            "sender": sender_wallet.data["name"],
            "receiver": receiver_wallet.data["name"],
            "transfer_amount": Decimal("1"),
        },
        format="json",
    )
    assert (
        Decimal(response.data["commission"]) == Decimal(response.data["transfer_amount"]) * Transaction.COMMISSION_RATE
    )
