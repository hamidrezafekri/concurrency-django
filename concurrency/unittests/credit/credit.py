import concurrent.futures
import json
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from rest_framework.response import Response

from concurrency.credit.models import CreditRequest
from concurrency.unittests.test_untils import generate_client, verified_customer, verified_seller1, verified_seller2, \
    admin, create_credit_request, create_product
from concurrency.users.models import BaseUser


class CreditTestCase(TestCase):

    def setUp(self):
        self.customer = verified_customer()
        self.customer_client = generate_client(self.customer)
        self.seller1 = verified_seller1()
        self.seller1_client = generate_client(self.seller1)
        self.seller2 = verified_seller2()
        self.seller2_client = generate_client(self.seller2)
        self.admin = admin()
        self.admin_client = generate_client(self.admin)

    def increate_credit_api(self, amount: int, seller: BaseUser, status: bool) -> Response:
        request = create_credit_request(seller=seller, amount=amount)
        url = reverse("api:credit:change-request-status", kwargs={"id": request.id})
        response = self.admin_client.put(url, {"status": status})
        return response

    def buy_product_api(self, amount: int, seller: BaseUser) -> Response:
        product = create_product(seller=seller, amount=amount)
        url = reverse("api:credit:buy-product-api")
        response = self.customer_client.post(url, json.dumps({"product": product.id}),
                                             content_type="application/json")
        return response

    def test_reject_increase_credit_request_seller1(self):
        response = self.increate_credit_api(amount=2000, seller=self.seller1, status=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.seller1.account_balance, 0.00)

    def test_increase_credit_seller1(self):
        response = self.increate_credit_api(amount=2000, seller=self.seller1, status=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.seller1.refresh_from_db()
        self.assertEqual(self.seller1.account_balance, 2000.00)

    def test_buy_product_seller1(self):
        response = self.increate_credit_api(amount=2000, seller=self.seller1, status=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.seller1.refresh_from_db()
        self.assertEqual(self.seller1.account_balance, 2000)
        response = self.buy_product_api(amount=1000, seller=self.seller1)
        self.customer.refresh_from_db()
        self.seller1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.customer.account_balance, 1000)
        self.assertEqual(self.seller1.account_balance, 1000)
        response = self.buy_product_api(seller=self.seller1, amount=1001)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_product_both_sellers(self):
        response = self.increate_credit_api(amount=10000, seller=self.seller1, status=True)
        self.seller1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.seller1.account_balance, 10000)
        response = self.increate_credit_api(amount=11000, seller=self.seller2, status=True)
        self.seller2.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.seller2.account_balance, 11000)
        response = self.buy_product_api(amount=5000, seller=self.seller1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.seller1.refresh_from_db()
        self.customer.refresh_from_db()
        self.assertEqual(self.seller1.account_balance, 5000)
        self.assertEqual(self.customer.account_balance, 5000)
        response = self.buy_product_api(amount=6000, seller=self.seller2)
        self.customer.refresh_from_db()
        self.seller2.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.customer.account_balance, 11000)
        self.assertEqual(self.seller2.account_balance, 5000)
