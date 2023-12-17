from django.contrib import admin

from concurrency.users.models import BaseUser


# Register your models here.
@admin.register(BaseUser)
class UserAdmin(admin.ModelAdmin):
    fields = ("firstname", "lastname", "phone_number", "account_balance", "phone_verified", "verified", "user_type")
    search_fields = ("phone_number" , "lastname" , "firstname")
    readonly_fields = ("account_balance" , "phone_number")
    list_display = (
    "firstname", "lastname", "phone_number", "account_balance", "phone_verified", "verified", "user_type")
    list_editable = ("phone_verified", "verified")
    list_filter = ("user_type", "firstname", "lastname", "phone_number")
