from django.db import transaction

from concurrency.credit.models import CreditRequest, Transaction, TransactionType, Product
from concurrency.credit.services.request import update_request_status
from concurrency.users.models import BaseUser
from concurrency.users.services import update_user_account_balance, increase_customer_balance


def create_credit_transaction(*, amount: int, seller_new_balance: int,
                              credit_request: CreditRequest) -> Transaction:
    return Transaction.objects.create(
        transaction_type=TransactionType.CREDIT,
        amount=amount,
        seller_new_balance=seller_new_balance,
        credit_request=credit_request
    )


def create_sell_transaction(*, amount: int, seller_new_balance: int, customer: BaseUser, customer_new_balance,
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
    credit_request.seller = BaseUser.objects.select_for_update().get(id=credit_request.seller.id)
    user = update_user_account_balance(user=credit_request.seller,
                                       amount=int(credit_request.amount),
                                       choice=TransactionType.CREDIT)

    create_credit_transaction(amount=int(credit_request.amount),
                              seller_new_balance=int(user.account_balance),
                              credit_request=credit_request)
    return credit_request


def reject_request(*, id: int) -> CreditRequest:
    credit_request = update_request_status(id=id, status=False)
    return credit_request


@transaction.atomic
def sell_product(*, customer: BaseUser, product_id: int) -> Transaction:
    product = Product.objects.get(id=product_id)
    product.seller = BaseUser.objects.select_for_update().get(id=product.seller.id)
    customer = BaseUser.objects.select_for_update().get(id=customer.id)
    seller = update_user_account_balance(user=product.seller
                                         , amount=product.amount,
                                         choice=TransactionType.SELL)

    customer = increase_customer_balance(customer=customer,
                                         amount=product.amount)

    transaction = create_sell_transaction(
        amount=product.amount,
        seller_new_balance=int(seller.account_balance),
        customer_new_balance=customer.account_balance,
        customer=customer,
        product=product
    )
    return transaction
