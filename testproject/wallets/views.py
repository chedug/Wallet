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

    def get_queryset(self):
        """
        This view should return a list of all
        wallets, where the user is current authenticated
        user.
        """
        user = self.request.user
        return Wallet.objects.all().filter(user=user.id)

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

    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Show only transactions where either receiver or sender
        wallet is of user's
        """
        queryset = Transaction.objects.filter(
            Q(sender__user=self.request.user.id)
            | Q(receiver__user=self.request.user.id)
        )
        return queryset

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
