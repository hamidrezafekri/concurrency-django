from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

import re



def phone_number_validator(phone_number):
    regex = re.compile('^(?:\+980)?9\d{9}$')
    if not regex.fullmatch(phone_number):
        raise ValidationError(
            _("enter valid phone_number")
        )
    
def number_validator(password):
    regex = re.compile('[0-9]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must include number"),
                code="password_must_include_number"
                )

def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must include letter"),
                code="password_must_include_letter"
                )

def special_char_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must include special char"),
                code="password_must_include_special_char"
                )

