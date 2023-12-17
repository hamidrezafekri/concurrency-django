from django.contrib import admin
from concurrency.credit.models import CreditRequest, Transaction, Product


@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    fields = ("status", "amount", "seller",)
    list_filter = ("status",)
    readonly_fields = ("status", "amount", "seller",)
    search_fields = ("seller",)
    list_display = ("seller", "amount", "status",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fields = (
        "transaction_type",
        "amount",
        "seller_new_balance",
        "customer_new_balance",
        "customer",
        "product",
        "credit_request",
        "created_at",
        "updated_at",

    )
    readonly_fields = (
        "transaction_type",
        "amount",
        "seller_new_balance",
        "customer_new_balance",
        "customer",
        "product",
        "credit_request",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "customer",
        "transaction_type",
        "amount",
        "created_at",
        "updated_at",
    )
    list_display = (
        "transaction_type",
        "amount",
        "created_at",
        "updated_at",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ("amount", "seller", "is_active", "created_at", "updated_at")
    readonly_fields = ("amount", "seller", "is_active", "created_at", "updated_at")
    list_display = ("seller", "amount", "is_active")
    search_fields = ("seller", "amount")
    list_filter = ("seller", "amount", "is_active", "created_at", "updated_at")
