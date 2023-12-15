from django.urls import path
from .apis import  (
                    UserRegisterApi,
                    VerifyPhoneApi,
                    VerifyPhoneRequestApi,
                    UserApi,
                    ChangePasswordRequestApi,
                    ChangePasswordApi,
        )


urlpatterns = [
    path('register/', UserRegisterApi.as_view(),name="seller-register"),
    path('request-verify-phone/' , VerifyPhoneRequestApi.as_view() , name= "request-verify-phone"),
    path('request-change-password/' ,ChangePasswordRequestApi.as_view() , name = "request-change_password"),
    path('verify-phone/' , VerifyPhoneApi.as_view() , name= "verify-phone"),
    path('change-password', ChangePasswordApi.as_view() , name= "change-password-api"),
    path('user/' , UserApi.as_view() , name = "user-api")

]
