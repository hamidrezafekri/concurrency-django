from django.db.models import F

from concurrency.users.models import BaseUser
from concurrency.credit.models import Product


def product_detail(seller: BaseUser, id: int) -> Product:
    return Product.objects.get(seller=seller, id=id)


def avalible_product_list() -> Product:
    return Product.objects.get(amount__lte=F('seller__account_balance'))
