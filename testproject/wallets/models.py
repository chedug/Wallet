from django.db import models

# Create your models here.
from django.db import models
from django.utils.crypto import get_random_string

TYPE_CHOICES = [("visa", "Visa"),
                ("mastercard", "Mastercard"), ]
CURRENCY_CHOICES = [("USD", "USD"),
                    ("EUR", "EUR"),
                    ("GBP", "GBP"), ]
allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def create_random_name():
    """Random 8 character long name"""
    return get_random_string(length=8, allowed_chars=allowed_chars)


class Wallet(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=8, blank=False,
                            unique=True, default=create_random_name)
    type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', related_name='wallets', on_delete=models.CASCADE)
    # TODO: Make default balance depend on currency

    class Meta:
        ordering = ["created_on"]
