"""
Transaction Business Logic
"""


def transaction(sender_wallet, receiver_wallet, transfer_amount):
    """Transaction between two wallets"""
    sender_wallet.balance -= transfer_amount
    receiver_wallet.balance += transfer_amount
    receiver_wallet.save()
    sender_wallet.save()
