# base
# installed
from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
# local
from apps.orderserviceapi import models


def get_object(model_or_queryset, **kwargs):
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None

# PROVIDER
def provider_get(provider_id) -> models.Provider | None:
    provider = get_object(models.Provider, id=provider_id)
    return provider

def provider_get_list() -> QuerySet:
    return models.Provider.objects.all()


# BUYER
def buyer_get(buyer_id) -> models.Buyer:
    return get_object(models.Buyer, id=buyer_id)


# PRODUCT
def product_get(product_id) -> models.Product | None:
    product = get_object(models.Product, id=product_id)
    return product

def product_remaining_stock_get(product_id: int) -> models.RemainingStock:
    remaining_stock = get_object(models.RemainingStock, product=product_id)
    return remaining_stock