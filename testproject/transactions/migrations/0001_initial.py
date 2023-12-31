# Generated by Django 4.2.4 on 2023-08-08 12:18

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wallets", "0003_delete_transaction"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transfer_amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=20,
                        validators=[
                            django.core.validators.MinValueValidator(
                                Decimal("0")
                            )
                        ],
                    ),
                ),
                (
                    "commission",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=20,
                        validators=[
                            django.core.validators.MinValueValidator(
                                Decimal("0")
                            )
                        ],
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("PAID", "Paid"), ("FAILED", "Failed")],
                        max_length=6,
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_transactions",
                        to="wallets.wallet",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_transactions",
                        to="wallets.wallet",
                    ),
                ),
            ],
            options={
                "ordering": ["timestamp"],
            },
        ),
    ]
