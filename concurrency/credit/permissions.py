from rest_framework.permissions import BasePermission
from concurrency.users.models import UserTypes

class SellerPermission(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.user.user_type == UserTypes.SELLER
