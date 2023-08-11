"""
Transaction Models
"""
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from wallets.models import Wallet

STATUS_CHOICES = [
    ("PAID", "Paid"),
    ("FAILED", "Failed"),
]


class Transaction(models.Model):
    """
    Represents a transaction between two Wallets.

    This model stores transaction entity between two wallets:
    - sender - wallet id
    - receiver - wallet id
    - transfer_amount - the amount of money that the "sender" sends to the "receiver". Example - 5.00
    - commission - 0.00 if no commission; otherwise, transfer_amount * 0.10
    - status - PAID if no problems; otherwise, FAILED
    - timestamp - datetime when the transaction was created
    """

    default_transfer_amount = Decimal("0")

    objects = models.Manager()
    sender = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="sender",
        to_field="name",
    )
    receiver = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="receiver",
        to_field="name",
    )
    transfer_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=default_transfer_amount,
        validators=[MinValueValidator(Decimal("0"))],
    )
    commission = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        editable=False,
        default=0,
        validators=[MinValueValidator(Decimal("0"))],
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=6, default="FAILED", editable=False
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, editable=False, null=False
    )

    class Meta:
        """
        Metadata and configuration options for Transaction model.
        """

        ordering = ["timestamp"]
