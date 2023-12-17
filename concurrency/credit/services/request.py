from concurrency.credit.models import CreditRequest, CreditRequestStatus
from concurrency.users.models import BaseUser


def request_increase_credit(*, seller: BaseUser, amount: float) -> CreditRequest:
    return CreditRequest.objects.create(seller=seller, amount=amount)


def update_request_status(*, id: int, status: bool) -> CreditRequest:
    return CreditRequest.objects.filter(id=id).update(
        status=CreditRequestStatus.APPROVED if status else CreditRequestStatus.REJECTED)
