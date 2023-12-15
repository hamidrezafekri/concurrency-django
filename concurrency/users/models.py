from enum import IntEnum

from django.db import models


from concurrency.common.models import BaseModel

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin


class VerifyType(IntEnum):
    PHONENUMBER = 1
    PASSWORD = 2

    @classmethod
    def choices(cls):
        return [(key.value , key.name) for key  in cls]


class UserTypes(IntEnum):
    CUSTOMER = 1
    SELLER = 2
    ADMIN  = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class BaseUserManager(BUM):
    def create_user(self, phone_number, firstname, lastname, is_active=True, is_admin=False, password=None , user_type = UserTypes.CUSTOMER):
        if not phone_number:
            raise ValueError("Users must have an phone_number")
        if not firstname:
            raise ValueError("users must have firstname")

        if not lastname:
            raise ValueError("Users must have lastname")

        user = self.model(phone_number=phone_number, firstname=firstname, lastname=lastname,
                          is_active=is_active, is_admin=is_admin ,user_type=user_type)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, firstname='test', lastname='test', password=None , user_type = None):
        user = self.create_user(
            phone_number=phone_number,
            firstname=firstname,
            lastname=lastname,
            is_active=True,
            is_admin=True,
            password=password,
            user_type=user_type,
        )

        user.is_superuser = True
        user.user_type = UserTypes.ADMIN
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    user_type = models.IntegerField(choices=UserTypes.choices(), default=UserTypes.CUSTOMER)
    firstname = models.CharField(verbose_name='first_name',
                                 max_length=100)
    lastname = models.CharField(verbose_name="last_name",
                                max_length=100)
    phone_number = models.CharField(verbose_name="phone_number",
                                    unique=True, max_length=11)
    phone_verified = models.BooleanField(default=False)
    verify_type = models.IntegerField(choices = VerifyType.choices(), null= True , blank = True)
    secret_key = models.CharField(max_length=100, null=True, blank=True)
    account_balance = models.DecimalField(
            max_digits=100 ,
            decimal_places=2,
            default = 0
        )
    verified = models.BooleanField(default = False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f'{self.firstname}-{self.lastname}'

    def is_staff(self):
        return self.is_admin

