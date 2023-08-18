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
    """
    Return 8-character-long random string.

    Characters are only uppercase English letters or digits 0-9.

    """
    random_name = get_random_string(length=8, allowed_chars=allowed_chars)
    while Wallet.objects.filter(name=random_name).exists():
        random_name = get_random_string(length=8, allowed_chars=allowed_chars)
    return random_name


class Wallet(models.Model):
    """
    Represents a Wallet of a user.

    This model stores wallet entity of users:
    - id
    - name - unique random 8 symbols of the Latin alphabet and digits. Example: MO72RTX3
    - type - 2 possible choices: Visa or Mastercard
    - currency - 3 possible choices: USD, EUR, GBP
    - balance - balance rounded up to 2 decimal places. Example: 1.38 - ok, 1.377 - wrong
    - user - user_id, who created the wallet
    - created_on - datetime when the wallet was created
    - modified_on - datetime when the wallet was modified
    """

    objects = models.Manager()

    MAX_NUMBER_OF_WALLETS = 5
    BONUSES = {
        "GBP": Decimal("100.00"),
        "USD": Decimal("3.00"),
        "EUR": Decimal("3.00"),
    }

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
        editable=False,
        null=False,
    )
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    modified_on = models.DateTimeField(auto_now=True, null=False)
    user = models.ForeignKey(
        "auth.User", related_name="wallets", on_delete=models.CASCADE
    )

    class Meta:
        """
        Metadata and configuration options for Wallet model.
        """

        ordering = ["created_on"]
