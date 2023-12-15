from .models import (
        BaseUser,
        VerifyType,
        )
import pyotp

def get_user(* , phone_number:str) -> BaseUser|None:
    return BaseUser.objects.get(phone_number = phone_number)


def verify_phone_otp( * , phone_number: str , otp:str) -> bool:
    try:
        user = BaseUser.objects.get(phone_number = phone_number)
    except BaseUser.DoesNotExist:
        return False
    if user.verify_type != VerifyType.PHONENUMBER:
        return False
    totp = pyotp.TOTP(s=user.secret_key , interval=120)
    return totp.verify(otp =str(otp))
