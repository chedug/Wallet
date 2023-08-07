"""
Views for Wallet app
"""

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions

from .models import Transaction, Wallet
from .permissions import IsOwnerOrReadOnly
from .serializers import (TransactionSerializer, UserSerializer,
                          WalletSerializer)


class WalletList(generics.ListCreateAPIView):
    """
    List Existing Wallets or add new
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WalletDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail of individual Wallet
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self):
        """
        GET Wallet or 404 if it doesn't exist
        """
        name = self.kwargs["name"]
        wallet = generics.get_object_or_404(Wallet, name=name)
        self.check_object_permissions(self.request, wallet)
        return wallet


class TransactionList(generics.ListCreateAPIView):
    """
    List existing transaction or add new one (curr. user)
    """

    serializer = TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Transaction.objects.filter(
            Q(sender__user=self.request.user) | Q(receiver__user=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
