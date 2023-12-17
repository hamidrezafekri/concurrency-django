from django.urls import path
from .apis.product import ProductApi, ProductDetailApi, ProductListApi
from .apis.request import CreditRequestApi
from .apis.transaction import ChangeRequestStatusApi

urlpatterns = [
    path("product/", ProductApi.as_view(), name="product-create-api"),
    path("product/<int:id>/", ProductDetailApi.as_view(), name="product-detail-api"),
    path('product-list/', ProductListApi.as_view(), name="product-list-api"),
    path('submit-request/', CreditRequestApi.as_view(), name="credit-request-api"),
    path("change-request-status/<int:id>/", ChangeRequestStatusApi.as_view(), name="change-request-status")
]
