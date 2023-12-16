from concurrency.credit.models import CreditRequest
from concurrency.users.models import BaseUser


def request_increase_credit(*, seller: BaseUser, amount: float) -> CreditRequest:
    return CreditRequest.objects.create(seller=seller, amount=amount)
