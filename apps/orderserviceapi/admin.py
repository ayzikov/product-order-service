from django.contrib import admin

from .models import Buyer


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    ...