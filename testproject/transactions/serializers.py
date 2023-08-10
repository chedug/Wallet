"""
Serializer for Transaction Model
"""


from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework import serializers
from wallets.models import Wallet

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction Model
    """

    # owner = serializers.ReadOnlyField(source="user.username")
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

    def create(self, validated_data):
        """
        Create transaction
        """
        self.validate_sender_and_receiver(validated_data)
        self.validate_currency(validated_data)
        self.validate_sender_money(validated_data)
        return Transaction.objects.create(**validated_data)

    def validate_sender_and_receiver(self, validated_data):
        """
        Validate that sender or receiver exists
        """
        sender_name = validated_data.get("sender").name
        receiver_name = validated_data.get("receiver").name
        try:
            Wallet.objects.get(name=sender_name)
            Wallet.objects.get(name=receiver_name)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError(
                "Provided sender/receiver does not exist"
            )

    def validate_currency(self, validated_data):
        """
        Checks if currencies are the same
        """
        sender = validated_data["sender"]
        receiver = validated_data["receiver"]
        sender_wallet = Wallet.objects.get(name=sender.name)
        receiver_wallet = Wallet.objects.get(name=receiver.name)
        if sender_wallet.currency != receiver_wallet.currency:
            raise serializers.ValidationError(
                "Wallets' currencies do not match."
            )

    def validate_sender_money(self, validated_data):
        """
        Validate that sender has enough money
        """
        sender = validated_data["sender"]
        transfer_amount = validated_data["transfer_amount"]
        sender_wallet = Wallet.objects.get(name=sender.name)

        if sender_wallet.balance - transfer_amount < Decimal("0"):
            raise serializers.ValidationError(
                f"User does not have enough money on wallet {sender}"
            )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for default auth.User model
    """

    transactions = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "transactions"]