from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.parsers import JSONParser
from wallets.models import Wallet
from wallets.serializers import WalletSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from wallets.permissions import IsOwnerOrReadOnly



class WalletList(generics.ListCreateAPIView):
    """
    List Existing Wallets
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WalletDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self):
        name = self.kwargs['name']
        wallet = generics.get_object_or_404(Wallet, name=name)
        self.check_object_permissions(self.request, wallet)
        return wallet


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
