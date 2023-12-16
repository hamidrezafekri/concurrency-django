from concurrency.users.models import BaseUser
from concurrency.credit.models import Product


def create_product(*, seller: BaseUser, amount: float, is_active: bool) -> Product:
    return Product.objects.create(
        seller=seller,
        amount=amount,
        is_active=is_active
    )


def update_product(*, id: int, amount: float, is_active: bool, ) -> Product:
    return Product.objects.get(id=id).update(amount=amount, is_active=is_active)
