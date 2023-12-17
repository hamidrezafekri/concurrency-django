from concurrency.credit.models import CreditRequest, CreditRequestStatus
from concurrency.users.models import BaseUser


def request_increase_credit(*, seller: BaseUser, amount: int) -> CreditRequest:
    return CreditRequest.objects.create(seller=seller, amount=amount)


def update_request_status(*, id: int, status: bool) -> CreditRequest:
    credit_request = CreditRequest.objects.get(id=id)
    credit_request.status = CreditRequestStatus.APPROVED if status else CreditRequestStatus.REJECTED
    return credit_request
