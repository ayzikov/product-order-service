# base
# installed
from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
# local
from apps.orderserviceapi.models import Provider, Product, RemainingStock


def get_object(model_or_queryset, **kwargs):
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None

# PROVIDER
def provider_get(provider_id) -> Provider | None:
    provider = get_object(Provider, id=provider_id)
    return provider

def provider_get_list() -> QuerySet:
    return Provider.objects.all()


# PRODUCT
def product_get(product_id) -> Product | None:
    product = get_object(Product, id=product_id)
    return product

def product_remaining_stock_get(product_id: int) -> RemainingStock:
    remaining_stock = get_object(RemainingStock, product=product_id)
    return remaining_stock