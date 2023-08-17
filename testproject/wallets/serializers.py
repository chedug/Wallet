"""
Serializers of the Wallets app
"""
from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for Wallet Model.

    Methods:
        create: Create an instance of Wallet.
        validate_max_wallets: Check that user does not have too many wallets.
        validate_bonus: Set bonus appropriately.
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True, source="user.username")

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
        Validate Wallet fields before serializing.
        """
        self.validate_max_wallets(validated_data)
        self.validate_bonus(validated_data)
        return Wallet.objects.create(**validated_data)

    def validate_max_wallets(self, validated_data):
        """
        User cannot have too many wallets.
        """
        user = validated_data["user"]
        if Wallet.objects.filter(user=user).count() >= Wallet.MAX_NUMBER_OF_WALLETS:
            raise serializers.ValidationError(f"Users can't create more than {Wallet.MAX_NUMBER_OF_WALLETS} wallets.")

    def validate_bonus(self, validated_data):
        """
        Adding bonus based on currency.
        """
        currency = validated_data.get("currency")
        bonus = Wallet.BONUSES[currency]  # Sets appropriate bonus for Wallet currency
        validated_data["balance"] = bonus
