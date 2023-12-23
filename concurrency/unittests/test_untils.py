from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from concurrency.users.models import (
    BaseUser,
    UserTypes,
)


def admin():
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


def customer():
    user = BaseUser.objects.create_user(
        phone_number="09101111111",
        password="@hamid14520",
        user_type=UserTypes.CUSTOMER,
        firstname="test1",
        lastname="test1"
    )
    return user


def verified_customer():
    user = BaseUser.objects.create_user(
        phone_number="09101111111",
        password="@hamid14520",
        user_type=UserTypes.CUSTOMER,
        firstname="test1",
        lastname="test1"
    )
    user.phone_verified = True
    user.save()
    return user


def seller1():
    user = BaseUser.objects.create_user(
        phone_number="09102222222",
        password="@hamid14520",
        user_type=UserTypes.SELLER,
        firstname="test1",
        lastname="test1"
    )
    return user


def verified_seller1():
    user = BaseUser.objects.create_user(
        phone_number="09102222222",
        password="@hamid14520",
        user_type=UserTypes.SELLER,
        firstname="test1",
        lastname="test1"
    )
    user.verified = True
    user.phone_verified = True
    user.save()
    return user


def seller2():
    user = BaseUser.objects.create_user(
        phone_number="09103333333",
        password="@hamid14520",
        user_type=UserTypes.SELLER,
        firstname="test1",
        lastname="test1"
    )
    return user


def verified_seller2():
    user = BaseUser.objects.create_user(
        phone_number="09103333333",
        password="@hamid14520",
        user_type=UserTypes.SELLER,
        firstname="test1",
        lastname="test1"
    )
    user.verified = True
    user.phone_verified = True
    user.save()
    return user


def generate_client(user: BaseUser) -> APIClient:
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


def customer_data() -> dict:
    payload = {
        "firstname": "customer-fn",
        "lastname": "customer-ln",
        "phone_number": "09101111111",
        "password": "@hamid14520",
        "confirm_password": "@hamid14520",
        "user_type": UserTypes.CUSTOMER,
    }
    return payload


def seller1_data() -> dict:
    payload = {
        "firstname": "seller1-fn",
        "lastname": "seller1-ln",
        "phone_number": "09102222222",
        "password": "@hamid14520",
        "confirm_password": "@hamid14520",
        "user_type": UserTypes.SELLER,
    }
    return payload


def seller2_data() -> dict:
    payload = {
        "firstname": "seller2-fn",
        "lastname": "seller2-ln",
        "phone_number": "09103333333",
        "password": "@hamid14520",
        "confirm_password": "@hamid14520",
        "user_type": UserTypes.SELLER,
    }
    return payload


def get_field(fieldname: str, value: int | str) -> dict:
    return {
        fieldname: value
    }
