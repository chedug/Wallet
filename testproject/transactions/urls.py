"""
Urls for Transactions app
"""

from django.urls import path
from transactions.views import TransactionList

urlpatterns = [
    path("wallets/transactions/", TransactionList.as_view()),
]
