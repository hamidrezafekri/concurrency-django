import json
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase

from concurrency.unittests.test_untils import generate_client, verified_customer, verified_seller1, verified_seller2, \
    admin, create_credit_request, create_product


class TransactionTestCase(TestCase):

    def setUp(self):
        self.customer = verified_customer()
        self.customer_client = generate_client(self.customer)
        self.seller1 = verified_seller1()
        self.seller1_client = generate_client(self.seller1)
        self.seller2 = verified_seller2()
        self.seller2_client = generate_client(self.seller2)
        self.admin = admin()
        self.admin_client = generate_client(self.admin)

    def test_reject_increase_credit_request_seller1(self):
        request = create_credit_request(seller=self.seller1, amount=2000)
        url = reverse("api:credit:change-request-status", kwargs={"id": request.id})
        response = self.admin_client.put(url, {"status": False})
        print(response.content)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(self.seller1.account_balance, 0.00)

    def test_increase_credit_seller1(self):
        request = create_credit_request(seller=self.seller1, amount=2000)
        url = reverse("api:credit:change-request-status", kwargs={"id": request.id})
        response = self.admin_client.put(url, {"status": True})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.seller1.refresh_from_db()
        self.assertEquals(self.seller1.account_balance, 2000.00)

    def test_buy_product_sellers(self):
        print(self.seller1.account_balance)
        product_seller1 = create_product(seller=self.seller1, amount=1000)
        product_seller2 = create_product(seller=self.seller2, amount=2000)
        url = reverse("api:credit:buy-product")
        response = self.customer_client.post(url  , json.dumps({"product": product_seller1.id}))
        self.assertEquals(response.status_code , )
