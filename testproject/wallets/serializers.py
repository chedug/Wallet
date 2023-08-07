"""
Serializers of the Wallets app
"""

from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for Wallet Model
    """

    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        """
        Related Model and its fields
        """

        model = Wallet
        fields = [
            "id",
            "name",
            "type",
            "currency",
            "balance",
            "user",
            "created_on",
            "modified_on",
        ]

    def create(self, validated_data):
        """
        Validate Wallet fields before serializing
        """
        self.validate_max_wallets(validated_data)
        self.validate_bonus(validated_data)
        return Wallet.objects.create(**validated_data)

    def validate_max_wallets(self, validated_data):
        """
        User cannot have more than 5 wallets
        """
        user = validated_data["user"]
        if Wallet.objects.filter(user=user).count() >= 5:
            raise serializers.ValidationError("Users can't create more than 5 wallets.")

    def validate_bonus(self, validated_data):
        """
        Adding bonus based on currency
        """
        currency = validated_data.get("currency")
        bonus = 0.00

        if currency == "GBP":
            bonus = Decimal(100.00)
        elif currency in ("USD", "EUR"):
            bonus = Decimal(3.00)

        balance = validated_data.get("balance")
        if balance is None:
            balance = 0.00
        validated_data["balance"] = balance + bonus


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction Model
    """

    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        """
        Related Model and its fields
        """

        model = Transaction
        fields = [
            "sender",
            "receiver",
            "transfer_amount",
            "commission",
            "status",
            "timestamp",
        ]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for default auth.User model
    """

    wallets = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["url", "id", "username", "wallets"]
