from .models import BaseUser
import pyotp
from concurrency.credit.models import TransactionType


def create_user(*, firstname: str, lastname: str, phone_number: str, password: str, user_type: int) -> BaseUser:
    return BaseUser.objects.create_user(
        firstname=firstname,
        lastname=lastname,
        phone_number=phone_number,
        password=password,
        user_type=user_type
    )


def update_user(*, user: BaseUser, firstname: str | None, lastname: str | None) -> None:
    user.firstname = firstname
    user.lastname = lastname
    user.save()


def update_user_secret(*, user: BaseUser, secret: str, verify_type: int) -> None:
    user.secret_key = secret
    user.verify_type = verify_type
    user.save()


def change_password(user: BaseUser, password) -> None:
    print(f"{password=}")
    user.set_password(password)
    user.full_clean()
    user.save()


def generate_otp(*, user: BaseUser, verify_type: int) -> str:
    secret = pyotp.random_base32()
    update_user_secret(user=user, secret=secret, verify_type=verify_type)
    totp = pyotp.TOTP(s=secret, interval=120)
    return totp.now()


def confirm_phone(*, phone_number: str) -> None:
    BaseUser.objects.filter(phone_number=phone_number).update(secret_key=None, verify_type=None, phone_verified=True)


class InsufficientFundsError(Exception):
    pass


def update_user_account_balance(user: BaseUser, amount: float, choice: int) -> BaseUser:
    if choice == TransactionType.CREDIT:
        user.account_balance += amount
    elif choice == TransactionType.SELL:
        if amount > user.account_balance:
            raise InsufficientFundsError(f"Cannot sell because amount exceeds user's account balance.")
        user.account_balance -= amount
    else:
        raise ValueError("Invalid transaction type.")
    user.save()
    return user
