from django.contrib import admin

from .models import Buyer, Order


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    ...


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ...