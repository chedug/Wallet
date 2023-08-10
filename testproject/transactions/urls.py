"""
Urls for Transactions app
"""

from django.urls import path
from transactions.views import (TransactionDetail, TransactionList,
                                TransactionWalletList)

urlpatterns = [
    path("wallets/transactions/", TransactionList.as_view()),
    path(
        "wallets/transactions/<int:id>",
        TransactionDetail.as_view(),
        name="transaction-detail",
    ),
    path(
        "wallets/transactions/<str:name>",
        TransactionWalletList.as_view(),
        name="transaction-wallets",
    ),
]
