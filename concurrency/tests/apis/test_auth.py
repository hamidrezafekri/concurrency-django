import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_customer_auth(api_customer):
    url = reverse("api:user:user-api")
    response = api_customer.get(url, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_seller1_auth(api_seller1):
    url = reverse("api:user:user-api")
    response = api_seller1.get(url, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_seller2_auth(api_seller2):
    url = reverse("api:user:user-api")
    response = api_seller2.get(url, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_admin_auth(api_admin):
    url = reverse("api:user:user-api")
    response = api_admin.get(url, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
