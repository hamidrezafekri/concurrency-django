from decimal import Decimal

import factory

from concurrency.credit.models import Product, CreditRequest, CreditRequestStatus
from concurrency.users.models import BaseUser, UserTypes


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseUser

    phone_number = factory.Sequence(lambda n: '1234567{}'.format(n))
    firstname = factory.Faker('first_name')
    lastname = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', '@hamid14520')

    @classmethod
    def create_seller(cls, **kwargs):
        return cls.create(user_type=UserTypes.SELLER, **kwargs)

    @classmethod
    def create_customer(cls, **kwargs):
        return cls.create(user_type=UserTypes.CUSTOMER, **kwargs)

    @classmethod
    def create_admin(cls, **kwargs):
        kwargs.setdefault('is_admin', True)
        kwargs.setdefault('is_active', True)
        return cls.create(user_type=UserTypes.ADMIN, **kwargs)

    @classmethod
    def create_superuser(cls, **kwargs):
        kwargs.setdefault('is_admin', True)
        kwargs.setdefault('is_active', True)
        return cls.create_superuser(**kwargs)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    amount = factory.LazyAttribute(lambda obj: Decimal('0.00'))
    seller = factory.SubFactory(BaseUserFactory, user_type=UserTypes.SELLER)
    is_active = True


class CreditRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CreditRequest

    status = CreditRequestStatus.PENDDING
    amount = factory.LazyAttribute(lambda obj: Decimal('0.00'))
    seller = factory.SubFactory(BaseUserFactory, user_type=UserTypes.SELLER)
