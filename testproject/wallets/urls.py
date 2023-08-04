from django.urls import path
from wallets.views import WalletList, UserList, UserDetail, WalletDetail


urlpatterns = [
    path('wallets/', WalletList.as_view()),
    path('wallets/<str:name>', WalletDetail.as_view(), name='wallet-detail'),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]
