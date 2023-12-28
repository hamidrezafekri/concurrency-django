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

from concurrency.users.models import UserTypes


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

    def test_register_with_not_equal_password(self):
        url = reverse("api:user:register")
        body={
            "firstname":"fname",
            "lastname":"lname",
            "phone_number":"09337272512",
            "password":"@hamid14520",
            "confirm_password":"@hamid1234",
            "user_type":UserTypes.CUSTOMER,
        }
        response = self.client.post(url , json.dumps(body) , content_type="application/json")
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)

    def test_register_wit_invalid_password(self):
        url = reverse("api:user:register")
        body = {
            "firstname": "fname",
            "lastname": "lname",
            "phone_number": "09337272512",
            "password": "hamid14520",
            "confirm_password": "hamid1234",
            "user_type": UserTypes.CUSTOMER,
        }
        response = self.client.post(url, json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)







