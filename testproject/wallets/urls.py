"""
Urls for Wallet app
"""

from django.urls import path
from wallets.views import (UserDetail, UserList, WalletDetail, WalletList,
                           schema_view)

urlpatterns = [
    path("", WalletList.as_view()),
    path("<str:name>", WalletDetail.as_view(), name="wallet-detail"),
    path("/", schema_view),
]
