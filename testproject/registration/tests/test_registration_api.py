"""
Tests for registration app
"""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.


class RegistrationTests(APITestCase):
    """
    Class for testing Registration
    """

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse("user-registration")
        data = {
            "username": "kazuyamishima",
            "password": "Qqwerty1!",
            "email": "nuralyhug@gmail.com",
            "first_name": "Kazuya",
            "last_name": "Mishima",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            User.objects.get(username="kazuyamishima").username,
            "kazuyamishima",
        )
