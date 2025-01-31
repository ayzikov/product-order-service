# base
# installed
# local
from apps.orderserviceapi import selectors
from apps.orderserviceapi.models import Provider
from apps.orderserviceapi.services import errors


# PROVIDER
def provider_create(data: dict) -> Provider:
    provider = Provider.objects.create(**data)
    return provider


def provider_modify(provider_id: int, data: dict) -> Provider:
    Provider.objects.filter(id=provider_id).update(**data)
    return Provider.objects.get(id=provider_id)


def provider_delete(provider_id: int) -> None:
    provider = selectors.provider_get(provider_id)
    if provider is None:
        errors.get_404_error(Provider)
    provider.delete()


