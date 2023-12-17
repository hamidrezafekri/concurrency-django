import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from concurrency.tests.factories import BaseUserFactory
from concurrency.users.models import BaseUser, UserTypes


@pytest.fixture
def api_seller1():
    user = BaseUser.objects.create_user(
        phone_number="09101111111",
        password="@hamid14520",
        user_type=UserTypes.SELLER,
        firstname="test1",
        lastname="test1"
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'{refresh.access_token}')
    return client

@pytest.fixture
def api_seller2():
    user = BaseUser.objects.create_user(
        phone_number="09102222222",
        password="@hamid14520",
        user_type=UserTypes.SELLER,
        firstname="test1",
        lastname="test1"
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'{refresh.access_token}')
    return client


@pytest.fixture
def api_customer():
    user = BaseUser.objects.create_user(
        phone_number="09103333333",
        password="@hamid14520",
        user_type=UserTypes.CUSTOMER,
        firstname="test1",
        lastname="test1"
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'{refresh.access_token}')
    return client


@pytest.fixture
def seller1():
    return BaseUserFactory()


@pytest.fixture
def user2():
    return BaseUserFactory()


@pytest.fixture
def profile1(user1):
    return ProfileFactory(user=user1)


@pytest.fixture
def subscription1(user1, user2):
    return SubscriptionFactory(target=user1, subscriber=user2)


@pytest.fixture
def post1(user1):
    return PostFactory(author=user1)
