"""
Transaction Views
"""


from django.db.models import Q
from rest_framework import generics, permissions
from transactions.logic import transaction

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionList(generics.ListCreateAPIView):
    """
    List existing transaction or add new one (curr. user)
    """

    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
        """
        Transfer money between two wallets
        """
        sender = serializer.validated_data["sender"]
        receiver = serializer.validated_data["receiver"]
        transfer_amount = serializer.validated_data["transfer_amount"]
        transaction(sender, receiver, transfer_amount)
        serializer.save()
