from django.db import transaction

from concurrency.credit.models import CreditRequest, Transaction, TransactionType, Product
from concurrency.credit.services.request import update_request_status
from concurrency.users.models import BaseUser
from concurrency.users.services import update_user_account_balance


def create_credit_transaction(*, amount: float, seller_new_balance: float,
                              credit_request: CreditRequest) -> Transaction:
    return Transaction.objects.create(
        transaction_type=TransactionType.CREDIT,
        amount=amount,
        seller_new_balance=seller_new_balance,
        credit_request=credit_request
    )


def create_sell_transaction(*, amount: float, seller_new_balance: float, customer: BaseUser, customer_new_balance,
                            product: Product) -> Transaction:
    return Transaction.objects.create(
        transaction_type=TransactionType.SELL,
        amount=amount,
        seller_new_balance=seller_new_balance,
        customer_new_balance=customer_new_balance,
        customer=customer,
        product=product,
    )


@transaction.atomic
def approve_request(*, id: int) -> CreditRequest:
    credit_request = update_request_status(id=id, status=True)
    user = update_user_account_balance(user=credit_request.seller,
                                       amount=float(credit_request.amount),
                                       choice=TransactionType.CREDIT)
    create_credit_transaction(amount=float(credit_request.amount),
                              seller_new_balance=float(user.account_balance),
                              credit_request=credit_request)
    return credit_request


def reject_request(*, id: int) -> CreditRequest:
    credit_request = update_request_status(id=id, status=False)
    return credit_request
