"""
Views for Wallet app
"""

from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework_swagger.views import get_swagger_view

from .models import Wallet
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, WalletSerializer


class WalletList(generics.ListCreateAPIView):
    """
    List Existing Wallets or add new
    """

    def get_queryset(self):
        """
        Only return those wallets, which belong to current user.
        """
        user = self.request.user
        return Wallet.objects.all().filter(user=user.id)

    serializer_class = WalletSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        """
        When creating a new wallet, set user field as current user.
        """
        serializer.save(user=self.request.user)


class WalletDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail of an individual Wallet.

    See info about wallet, update it or destroy the wallet.
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def get_object(self):
        """
        GET Wallet or 404 if it doesn't exist
        """
        name = self.kwargs["name"]
        wallet = generics.get_object_or_404(Wallet, name=name)
        self.check_object_permissions(self.request, wallet)
        return wallet


class UserList(generics.ListAPIView):
    """
    User List View
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    User Detail View
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


schema_view = get_swagger_view(title="Wallet-Transactions API")
