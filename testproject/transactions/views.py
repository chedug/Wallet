"""
Transaction Views
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.query import QuerySet
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from testproject.permissions import IsSenderOwner
from transactions.utils import commission_calculation, wallet_transaction

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionList(generics.ListCreateAPIView):
    """
    List existing transaction or add new one (curr. user)
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsSenderOwner]

    serializer_class = TransactionSerializer

    def get_queryset(self) -> QuerySet[Transaction]:
        """
        Show only transactions where either receiver or sender
        wallet is of user's
        """
        queryset = Transaction.objects.filter(
            Q(sender__user=self.request.user.id) | Q(receiver__user=self.request.user.id)
        )
        return queryset

    def perform_create(self, serializer: TransactionSerializer) -> None:
        """
        Transfer money between two wallets
        """
        transfer_amount = serializer.validated_data.get("transfer_amount", Transaction.default_transfer_amount)
        sender = serializer.validated_data["sender"]
        receiver = serializer.validated_data["receiver"]
        commission = commission_calculation(sender, receiver, transfer_amount)
        serializer.validated_data["commission"] = commission
        try:
            wallet_transaction(sender, receiver, transfer_amount, commission)
            serializer.save(status="PAID")
        except ObjectDoesNotExist:
            raise ValidationError
        except ValidationError:
            serializer.save(status="FAILED")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TransactionDetail(generics.RetrieveDestroyAPIView):
    """
    Detail of individual Transaction
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_object(self) -> Transaction:
        """
        Get Transaction or 404 if it doesn't exist
        """
        transaction_id = self.kwargs["id"]
        transaction = generics.get_object_or_404(Transaction, id=transaction_id)
        self.check_object_permissions(self.request, transaction)
        return transaction


class TransactionWalletList(generics.ListAPIView):
    """
    All transactions where wallet was sender or receiver
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self) -> QuerySet[Transaction]:
        wallet_name = self.kwargs["name"]
        queryset = Transaction.objects.filter(Q(sender__name=wallet_name) | Q(receiver__name=wallet_name))
        return queryset
