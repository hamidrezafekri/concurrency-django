from concurrent.futures import ThreadPoolExecutor

import pytest
from django.urls import reverse
import json

from rest_framework import status


@pytest.mark.django_db
def test_order_product_zero_balance_seller_one(api_customer, seller_one_product_1000):
    url = reverse("api:credit:buy-product-api")
    body = {"product": seller_one_product_1000.id}
    response = api_customer.post(url, json.dumps(body), content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_order_product_zero_balance_seller_two(api_customer, seller_two_product_10000):
    url = reverse("api:credit:buy-product-api")
    body = {"product": seller_two_product_10000.id}
    response = api_customer.post(url, json.dumps(body), content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_approve_credit_request_seller_one(api_admin, seller_one_credit_2000, seller1):
    url = reverse("api:credit:change-request-status", kwargs={"id": seller_one_credit_2000.id})
    body = {"status": True}
    response = api_admin.put(url, json.dumps(body), content_type="application/json")
    seller1.refresh_from_db()
    assert seller1.account_balance == seller_one_credit_2000.amount
    assert response.status_code == status.HTTP_200_OK

# @pytest.mark.django_db
# def test_concurrent_requests(api_admin, seller_one_credit_2000, seller1):
#     def hit_endpoint():
#         url = reverse("api:credit:change-request-status", kwargs={"id": seller_one_credit_2000.id})
#         body = {"status": True}
#         response = api_admin.put(url, json.dumps(body), content_type="application/json")
#         assert response.status_code == 200
#         seller1.refresh_from_db()
#         assert seller1.account_balance == 4000
#
#     request_count = 2
#     with ThreadPoolExecutor(max_workers=request_count) as executor:
#         futures = [executor.submit(hit_endpoint) for _ in range(request_count)]
#
#     for future in futures:
#         future.result()
