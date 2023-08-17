"""
Views for Registration app
"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegistrationSerializer


class UserRegistrationView(CreateAPIView):
    """
    Registration View
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """
        When user is created, its tokens will be shown
        """
        username = request.data["username"]
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            user = User.objects.get(username=username)
            refresh = RefreshToken.for_user(user)
            response.data["access_token"] = str(refresh.access_token)
            response.data["refresh_token"] = str(refresh)
        return response
