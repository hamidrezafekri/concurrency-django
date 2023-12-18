import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from concurrency.tests.factories import ProductFactory, CreditRequestFactory
from concurrency.users.models import BaseUser, UserTypes


@pytest.fixture
def seller1(db):
    user = BaseUser.objects.create_user(
        phone_number="09101111111",
        password="@hamid14520",
        user_type=UserTypes.SELLER,
        firstname="test1",
        lastname="test1"
    )
    user.phone_verified = True
    user.verified = True
    user.save()
    return user


@pytest.fixture
def api_seller1(seller1, db):
    client = APIClient()
    refresh = RefreshToken.for_user(seller1)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def seller2(db):
    user = BaseUser.objects.create_user(
        phone_number="09102222222",
        password="@hamid14520",
        user_type=UserTypes.SELLER,
        firstname="test1",
        lastname="test1"
    )
    user.phone_verified = True
    user.verified = True
    user.save()
    return user


@pytest.fixture
def api_seller2(seller2, db):
    client = APIClient()
    refresh = RefreshToken.for_user(seller2)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def customer(db):
    user = BaseUser.objects.create_user(
        phone_number="09103333333",
        password="@hamid14520",
        user_type=UserTypes.CUSTOMER,
        firstname="test1",
        lastname="test1"
    )
    user.phone_verified = True
    user.verified = True
    user.save()
    return user


@pytest.fixture
def api_customer(customer, db):
    client = APIClient()
    refresh = RefreshToken.for_user(customer)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def admin(db):
    user = BaseUser.objects.create_user(
        phone_number="09104444444",
        password="@hamid14520",
        user_type=UserTypes.ADMIN,
        firstname="test1",
        lastname="test1"
    )
    user.phone_verified = True
    user.verified = True
    user.is_admin = True
    user.save()

    return user


@pytest.fixture
def api_admin(admin, db):
    client = APIClient()
    refresh = RefreshToken.for_user(admin)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def seller_one_product_1000(seller1, db):
    return ProductFactory(amount=1000, seller=seller1)


@pytest.fixture
def seller_one_product_1500(seller1, db):
    return ProductFactory(amount=1500, seller=seller1)


@pytest.fixture
def seller_one_product_5000(seller1, db):
    return ProductFactory(amount=5000, seller=seller1)


@pytest.fixture
def seller_one_product_6000(seller1, db):
    return ProductFactory(amount=6000, seller=seller1)


@pytest.fixture
def seller_one_product_10000(seller1, db):
    return ProductFactory(amount=10000, seller=seller1)


@pytest.fixture
def seller_two_product_1000(seller2, db):
    return ProductFactory(amount=1000, seller=seller2)


@pytest.fixture
def seller_two_product_3000(seller2, db):
    return ProductFactory(amount=3000, seller=seller2)


@pytest.fixture
def seller_two_product_5000(seller2, db):
    return ProductFactory(amount=5000, seller=seller2)


@pytest.fixture
def seller_two_product_6000(seller2, db):
    return ProductFactory(amount=6000, seller=seller2)


@pytest.fixture
def seller_two_product_10000(seller2, db):
    return ProductFactory(amount=10000, seller=seller2)


@pytest.fixture
def seller_one_credit_100000(seller1, db):
    return CreditRequestFactory(amount=100000, seller=seller1)


@pytest.fixture
def seller_one_credit_2000(seller1, db):
    return CreditRequestFactory(amount=2000, seller=seller1)


@pytest.fixture
def seller_two_credit_60000(seller2, db):
    return CreditRequestFactory(amount=60000, seller=seller2)


@pytest.fixture
def seller_two_credit_5000(db, seller2):
    return CreditRequestFactory(amount=5000, seller=seller2)
