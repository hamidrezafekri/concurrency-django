from django.test import TestCase
from rest_framework import status

from concurrency.unittests.test_untils import (
    seller1_data,
    seller2_data,
    customer_data,
)
from rest_framework.test import APIClient
from django.urls import reverse
import json
class UsersRegisterTest(TestCase):

    def setUp(self):
        self.seller1 = seller1_data()
        self.seller2 = seller2_data()
        self.customer = customer_data()
        self.client = APIClient()

    def test_register_seller1(self):
        url = reverse("api:user:register")
        response = self.client.post(url , json.dumps(self.seller1) , content_type="application/json")
        self.assertEquals(response.status_code , status.HTTP_200_OK)

    def test_register_seller2(self):
        url = reverse("api:user:register")
        response = self.client.post(url, json.dumps(self.seller2), content_type="application/json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_register_customer(self):
        url = reverse("api:user:register")
        response = self.client.post(url, json.dumps(self.customer), content_type="application/json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)






