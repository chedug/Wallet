"""
Transaction Business Logic
"""
from decimal import Decimal

from django.db import transaction
from rest_framework import serializers


@transaction.atomic
def wallet_transaction(
    sender_wallet, receiver_wallet, transfer_amount, commission
):
    """Transaction between two wallets"""
    if sender_wallet.balance - transfer_amount < Decimal("0"):
        raise serializers.ValidationError(
            f"User does not have enough money on wallet {sender_wallet.name}"
        )

    sender_wallet.balance -= transfer_amount + commission
    receiver_wallet.balance += transfer_amount
    receiver_wallet.save()
    sender_wallet.save()


def commission_calculation(sender, receiver, transfer_amount):
    if sender.user == receiver.user:
        return Decimal("0")
    return transfer_amount * Decimal("0.1")
