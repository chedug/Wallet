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
        This view should return a list of all
        wallets, where the user is current authenticated
        user.
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
        Set user field as current user
        """
        serializer.save(user=self.request.user)


class WalletDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail of individual Wallet
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
