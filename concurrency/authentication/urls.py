from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from concurrency.authentication.apis import (
    CustomerLoginApi,
    SellerLoginApi, AdminLoginApi,
)
urlpatterns = [
        path('jwt/', include(([
            path('cutomer-login/', CustomerLoginApi.as_view(),name="login"),
            path('seller-login/' , SellerLoginApi.as_view() , name = "seller-login"),
            path("admin-login/" , AdminLoginApi.as_view() , name= "admin-login"),
            path('refresh/', TokenRefreshView.as_view(),name="refresh"),
            path('verify/', TokenVerifyView.as_view(),name="verify"),
            ])), name="jwt"),
        ]
