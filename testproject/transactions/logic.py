"""
Transaction Business Logic
"""
from django.db import transaction


@transaction.atomic
def wallet_transaction(sender_wallet, receiver_wallet, transfer_amount):
    """Transaction between two wallets"""
    sender_wallet.balance -= transfer_amount
    receiver_wallet.balance += transfer_amount
    receiver_wallet.save()
    sender_wallet.save()
