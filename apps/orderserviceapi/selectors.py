# base
# installed
from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
# local
from apps.orderserviceapi.models import Provider


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