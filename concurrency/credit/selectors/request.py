from concurrency.credit.models import CreditRequest
from concurrency.users.models import BaseUser


def seller_request_list(*, seller: BaseUser) -> CreditRequest:
    return CreditRequest.objects.get(seller=seller)


def get_last_request() -> CreditRequest:
    return CreditRequest.objects.last()
