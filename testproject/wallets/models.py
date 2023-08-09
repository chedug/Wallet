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

    objects = models.Manager()
    max_number_of_wallets = 5

    name = models.CharField(
        max_length=8,
        blank=False,
        unique=True,
        editable=False,
        default=create_random_name,
    )
    type = models.CharField(
        choices=TYPE_CHOICES, default="visa", max_length=10
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, default="USD", max_length=3
    )
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(Decimal("0"))],
    )
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    modified_on = models.DateTimeField(auto_now=True, null=False)
    user = models.ForeignKey(
        "auth.User", related_name="wallets", on_delete=models.CASCADE
    )

    class Meta:
        """
        Order by creation datetime
        """

        ordering = ["created_on"]

    def create_random_name(self):
        """Random 8 character long name"""
        random_name = get_random_string(length=8, allowed_chars=allowed_chars)
        while Wallet.objects.filter(name=random_name).exists():
            random_name = get_random_string(
                length=8, allowed_chars=allowed_chars
            )
        return random_name
