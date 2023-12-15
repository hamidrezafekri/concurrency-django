from .models import BaseUser
import pyotp

def create_user(* , firstname:str , lastname:str , phone_number:str , password:str , user_type:int) -> BaseUser:
    return BaseUser.objects.create_user(
            firstname = firstname,
            lastname = lastname,
            phone_number= phone_number,
            password = password,
            user_type = user_type
            )
def update_user(* ,user:BaseUser, firstname:str|None , lastname:str|None) -> None:
    user.firstname = firstname
    user.lastname = lastname
    user.save()


def update_user_secret(*, user: BaseUser, secret: str, verify_type: int) -> None:
    user.secret_key = secret
    user.verify_type = verify_type
    user.save()


def generate_otp(*, user: BaseUser, verify_type: int) -> str:
    secret = pyotp.random_base32()
    update_user_secret(user=user, secret=secret, verify_type=verify_type)
    totp = pyotp.TOTP(s=secret, interval=120)
    return totp.now()

def confirm_phone(*, phone_number: str) -> None:
    BaseUser.objects.filter(phone_number=phone_number).update(secret_key=None, verify_type=None, phone_verified=True)
