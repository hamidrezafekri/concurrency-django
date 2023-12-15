from django.urls import path
from .apis import  UserRegisterApi, VerifyPhoneApi , VerifyPhoneRequestApi , UserApi


urlpatterns = [
    path('register/', UserRegisterApi.as_view(),name="seller-register"),
    path('request-verify-phone/' , VerifyPhoneRequestApi.as_view() , name= "request-verify-phone"),
    path('verify-phone/' , VerifyPhoneApi.as_view() , name= "verify-phone"),
    path('user/' , UserApi.as_view() , name = "user-api")

]
