"""
Wallet app Models
"""


from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.crypto import get_random_string

TYPE_CHOICES = [
    ("visa", "Visa"),
    ("mastercard", "Mastercard"),
]
CURRENCY_CHOICES = [
    ("USD", "USD"),
    ("EUR", "EUR"),
    ("GBP", "GBP"),
]
allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
STATUS_CHOICES = [
    ("PAID", "Paid"),
    ("FAILED", "Failed"),
]


def create_random_name():
    """Random 8 character long name"""
    random_name = get_random_string(length=8, allowed_chars=allowed_chars)
    while Wallet.objects.filter(name=random_name).exists():
        random_name = get_random_string(length=8, allowed_chars=allowed_chars)
    return random_name


class Wallet(models.Model):
    """
    User Wallets
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=8,
        blank=False,
        unique=True,
        editable=False,
        default=create_random_name,
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3)
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(Decimal("0"))],
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "auth.User", related_name="wallets", on_delete=models.CASCADE
    )

    class Meta:
        """
        Order by creation datetime
        """

        ordering = ["created_on"]


class Transaction(models.Model):
    """
    Transaction between wallets
    """

    sender = models.ForeignKey(
        "Wallet", on_delete=models.CASCADE, related_name="sent_transactions"
    )
    receiver = models.ForeignKey(
        "Wallet", on_delete=models.CASCADE, related_name="received_transactions"
    )
    transfer_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    commission = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Order by datetime
        """

        ordering = ["timestamp"]
