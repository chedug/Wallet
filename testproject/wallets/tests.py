"""
Testing wallets app
"""


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.


class TestWalletAPI(APITestCase):
    """
    Class for testing wallets
    """

    def test_create_wallet(self):
        """
        Test that wallet is created
        """
        url = reverse("token-obtain-pair")
        data = {"type": "visa", "currency": "GBP"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
