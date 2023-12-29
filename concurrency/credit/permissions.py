from rest_framework.permissions import BasePermission
from concurrency.users.models import UserTypes


class SellerPermission(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.user.user_type == UserTypes.SELLER




class AdminPermission(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.user.user_type == UserTypes.ADMIN and request.user.is_admin


class CustomerPermission(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.user.user_type == UserTypes.CUSTOMER
