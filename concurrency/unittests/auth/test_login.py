from rest_framework import status
from django.test import TestCase
from django.urls import reverse
import json
from concurrency.unittests.test_untils import admin, verified_customer, verified_seller1, verified_seller2
from rest_framework.test import APIClient


class UserLoginTest(TestCase):

    def setUp(self) -> None:
        self.customer = verified_customer()
        self.seller1 = verified_seller1()
        self.seller2 = verified_seller2()
        self.admin = admin()
        self.client = APIClient()

    def test_login_not_exists_customer(self):
        url = reverse("api:auth:jwt:login")
        body = {
            "phone_number": "09121111111",
            "password": "@hamid14520"
        }
        response = self.client.post(url, json.dumps(body), content_type="application/json")
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_customer_with_admin(self):
        url = reverse("api:auth:jwt:login")
        body = {
            "phone_number": self.admin.phone_number,
            "password": "@hamid14520"
        }
        response = self.client.post(url, json.dumps(body), content_type="application/json")
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_admin_with_customer(self):
        url = reverse("api:auth:jwt:admin-login")
        body = {
            "phone_number": self.customer.phone_number,
            "password": "@hamid14520"
        }
        response = self.client.post(url, json.dumps(body), content_type="application/json")
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_customer_incorrect_password(self):
        url = reverse("api:auth:jwt:login")
        body = {
            "phone_number": self.customer.phone_number,
            "password": "@hamid1452"
        }
        response = self.client.post(url, json.dumps(body), content_type="application/json")
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_customer(self):
        url = reverse("api:auth:jwt:login")
        body = {
            "phone_number": self.customer.phone_number,
            "password": "@hamid14520"
        }
        response = self.client.post(url, json.dumps(body), content_type="application/json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_login_seller1(self):
        url = reverse("api:auth:jwt:seller-login")
        body = {
            "phone_number": self.seller1.phone_number,
            "password": "@hamid14520"
        }
        response = self.client.post(url, json.dumps(body), content_type="application/json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_login_seller2(self):
        url = reverse("api:auth:jwt:seller-login")
        body = {
            "phone_number": self.seller2.phone_number,
            "password": "@hamid14520"
        }
        response = self.client.post(url, json.dumps(body), content_type="application/json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
