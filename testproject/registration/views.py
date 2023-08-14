"""
Views for Registration app
"""
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView

from .serializers import UserRegistrationSerializer


class UserRegistrationView(CreateAPIView):
    """
    Registration View
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
