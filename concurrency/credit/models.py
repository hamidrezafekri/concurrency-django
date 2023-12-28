from django.db import models
from concurrency.common.models import BaseModel
from concurrency.users.models import BaseUser
from enum import IntEnum


class CreditRequestStatus(IntEnum):
    PENDDING = 1
    APPROVED = 2
    REJECTED = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class TransactionType(IntEnum):
    SELL = 1
    CREDIT = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class CreditRequest(BaseModel):
    status = models.IntegerField(choices=CreditRequestStatus.choices(), default=CreditRequestStatus.PENDDING)
    amount = models.DecimalField(max_digits=15,
                                 decimal_places=2,
                                 )
    seller = models.ForeignKey(to=BaseUser, on_delete=models.CASCADE,
                               related_name="creditrequest")

    def __str__(self):
        return f"{self.seller.lastname}-{self.amount}-{self.status}"


class Transaction(BaseModel):
    transaction_type = models.IntegerField(
        choices=TransactionType.choices(),
    )
    amount = models.DecimalField(max_digits=15,
                                 decimal_places=2,
                                 )
    customer = models.ForeignKey(
        BaseUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions_as_customer",
    )
    seller_new_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )
    customer_new_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
    )

    product = models.ForeignKey("Product",
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True
                                )
    credit_request = models.OneToOneField("CreditRequest",
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True
                                          )


class Product(BaseModel):
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )
    seller = models.ForeignKey(BaseUser, on_delete=models.CASCADE,
                               related_name="products")
    is_active = models.BooleanField()
