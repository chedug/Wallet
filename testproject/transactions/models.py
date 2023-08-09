# Create your models here.
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
    Transaction between wallets
    """

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
        default=0.00,
        validators=[MinValueValidator(Decimal("0"))],
    )
    commission = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        editable=False,
        default=0.00,
        validators=[MinValueValidator(Decimal("0"))],
    )
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=6, default="FAILED"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, editable=False, null=False
    )

    class Meta:
        """
        Order by datetime
        """

        ordering = ["timestamp"]
