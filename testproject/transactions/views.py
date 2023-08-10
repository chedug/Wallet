"""
Transaction Views
"""


from decimal import Decimal

from django.db.models import Q
from rest_framework import generics, permissions, serializers
from transactions.logic import commission_calculation, wallet_transaction

from .models import Transaction
from .permissions import IsOwnerOrReadOnly
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
        try:
            transfer_amount = serializer.validated_data["transfer_amount"]
        except KeyError:
            """in case transfer amount is not specified"""
            transfer_amount = Transaction.default_transfer_amount
        sender = serializer.validated_data["sender"]
        receiver = serializer.validated_data["receiver"]
        commission = commission_calculation(sender, receiver, transfer_amount)
        try:
            wallet_transaction(sender, receiver, transfer_amount, commission)
            serializer.save(status="PAID")
        except serializers.ValidationError:
            serializer.save(status="FAILED")


class TransactionDetail(generics.RetrieveDestroyAPIView):
    """
    Detail of individual Transaction
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        """
        Get Transaction or 404 if it doesn't exist
        """
        transaction_id = self.kwargs["id"]
        transaction = generics.get_object_or_404(
            Transaction, id=transaction_id
        )
        self.check_object_permissions(self.request, transaction)
        return transaction


class TransactionWalletList(generics.ListAPIView):
    """
    All transactions where wallet was sender or receiver
    """

    serializer_class = TransactionSerializer

    def get_queryset(self):
        wallet_name = self.kwargs["name"]
        queryset = Transaction.objects.filter(
            Q(sender__name=wallet_name) | Q(receiver__name=wallet_name)
        )
        return queryset
