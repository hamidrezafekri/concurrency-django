from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from concurrency.unittests.test_untils import customer, seller1, seller2
import json


class VerifyUserTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def post_request(self, url_name, data):
        url = reverse(url_name)
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        return response

    def verify_phone_number(self, user_factory):
        user = user_factory()
        request_otp_response = self.post_request("api:user:request-verify-phone", {"phone_number": user.phone_number})
        self.assertEqual(request_otp_response.status_code, status.HTTP_200_OK)
        otp = str(request_otp_response.content).split("=")[1][2:8]

        verify_response = self.post_request("api:user:verify-phone", {
            "phone_number": user.phone_number,
            "otp": otp
        })
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)

    def test_request_otp_with_not_exists_number(self):
        response = self.post_request("api:user:request-verify-phone", {"phone_number": "09121111111"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_verify_phone(self):
        self.verify_phone_number(customer)

    def test_seller1_verify_phone(self):
        self.verify_phone_number(seller1)

    def test_seller2_verify_phone(self):
        self.verify_phone_number(seller2)

    def test_verify_with_incorrect_otp(self):
        user = seller1()
        verify_response = self.post_request("api:user:verify-phone", {
            "phone_number": user.phone_number,
            "otp": 123456
        })
        self.assertEqual(verify_response.status_code, status.HTTP_400_BAD_REQUEST)
