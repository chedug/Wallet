"""
Urls for Transactions app
"""

from django.urls import path
from transactions.views import TransactionDetail, TransactionList, TransactionWalletList

urlpatterns = [
    path("", TransactionList.as_view(), name="transaction-list"),
    path(
        "<int:id>",
        TransactionDetail.as_view(),
        name="transaction-detail",
    ),
    path(
        "<str:name>",
        TransactionWalletList.as_view(),
        name="transaction-wallets",
    ),
]
