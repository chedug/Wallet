"""
Urls for Wallet app
"""

from django.urls import path
from wallets.views import WalletDetail, WalletList

urlpatterns = [
    path("", WalletList.as_view(), name="wallet-list-create"),
    path("<str:name>", WalletDetail.as_view(), name="wallet-detail"),
]
