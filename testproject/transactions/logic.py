"""
Transaction Business Logic
"""
from decimal import Decimal

from django.db import transaction


@transaction.atomic
def wallet_transaction(
    sender_wallet, receiver_wallet, transfer_amount, commission
):
    """Transaction between two wallets"""
    sender_wallet.balance -= transfer_amount + commission
    receiver_wallet.balance += transfer_amount
    receiver_wallet.save()
    sender_wallet.save()


def commission_calculation(sender, receiver, transfer_amount):
    if sender.user == receiver.user:
        return Decimal("0")
    return transfer_amount * Decimal("0.1")
