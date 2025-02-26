# base
# installed
from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404
# local
from apps.orderserviceapi import models


def get_object(model_or_queryset, **kwargs):
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None

def get_objects_list(model, **kwargs):
    try:
        return get_list_or_404(model, **kwargs)
    except Http404:
        return []


# PROVIDER
def provider_get(provider_id) -> models.Provider | None:
    provider = get_object(models.Provider, id=provider_id)
    return provider

def provider_get_list() -> list:
    return get_objects_list(models.Provider)


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


# ORDER
def order_get(order_id: int) -> models.Order:
    return get_object(models.Order, id=order_id)

def product_in_order_get(order_id: int, product_id: int) -> models.ProductOrder:
    return get_object(models.ProductOrder, order=order_id, product=product_id)

def products_in_order_get_list(order_id: int) -> list:
    return get_objects_list(models.ProductOrder, order_id=order_id)