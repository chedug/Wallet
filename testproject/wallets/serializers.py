from rest_framework import serializers
from wallets.models import Wallet
from django.contrib.auth.models import User


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Wallet
        fields = ['id', 'name', 'type', 'currency', 'balance', 'user', 'created_on', 'modified_on', ]


class UserSerializer(serializers.ModelSerializer):
    wallets = serializers.RelatedField(many=True, read_only=True )

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'wallets']