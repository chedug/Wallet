"""
Urls for Wallet app
"""

from django.urls import path
from wallets.views import (TransactionList, UserDetail, UserList, WalletDetail,
                           WalletList)

urlpatterns = [
    path("wallets/", WalletList.as_view()),
    path("wallets/<str:name>", WalletDetail.as_view(), name="wallet-detail"),
    path("wallets/transactions/", TransactionList.as_view()),
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
]
