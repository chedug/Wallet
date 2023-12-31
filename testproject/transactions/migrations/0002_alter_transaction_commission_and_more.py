# Generated by Django 4.2.4 on 2023-08-08 15:11

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wallets", "0004_alter_wallet_currency_alter_wallet_id_and_more"),
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="commission",
            field=models.DecimalField(
                decimal_places=2,
                editable=False,
                max_digits=20,
                validators=[
                    django.core.validators.MinValueValidator(Decimal("0"))
                ],
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="receiver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="receiver",
                to="wallets.wallet",
                to_field="name",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sender",
                to="wallets.wallet",
                to_field="name",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.CharField(
                choices=[("PAID", "Paid"), ("FAILED", "Failed")],
                default="FAILED",
                max_length=6,
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="transfer_amount",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=20,
                validators=[
                    django.core.validators.MinValueValidator(Decimal("0"))
                ],
            ),
        ),
    ]
