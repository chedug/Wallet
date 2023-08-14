"""
Views for Wallet app
"""

from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from testproject.permissions import IsOwner

from .models import Wallet
from .serializers import WalletSerializer


class WalletList(generics.ListCreateAPIView):
    """
    List Existing Wallets or add new
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = WalletSerializer

    def get_queryset(self):
        """
        Only return those wallets, which belong to current user.
        """
        user = self.request.user
        return Wallet.objects.all().filter(user=user.id)

    def perform_create(self, serializer):
        """
        When creating a new wallet, set user field as current user.
        """
        serializer.save(user=self.request.user)


class WalletDetail(generics.RetrieveDestroyAPIView):
    """
    Detail of an individual Wallet.

    See info about wallet, update it or destroy the wallet.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get_object(self):
        """
        GET Wallet or 404 if it doesn't exist
        """
        name = self.kwargs["name"]
        wallet = generics.get_object_or_404(Wallet, name=name)
        self.check_object_permissions(self.request, wallet)
        return wallet
