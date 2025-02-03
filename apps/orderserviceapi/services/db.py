# base
# installed
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
# local
from apps.orderserviceapi import selectors
from apps.orderserviceapi import models
from apps.orderserviceapi.services import errors, tasks


# PROVIDER
def provider_create(data: dict) -> models.Provider:
    provider = models.Provider.objects.create(**data)
    return provider

def provider_modify(provider_id: int, data: dict) -> models.Provider:
    models.Provider.objects.filter(id=provider_id).update(**data)
    return models.Provider.objects.get(id=provider_id)

def provider_delete(provider_id: int) -> None:
    provider = selectors.provider_get(provider_id)
    if provider is None:
        errors.get_404_error(models.Provider)
    provider.delete()


# BUYER
def buyer_create(request: Request, data: dict) -> models.Buyer:
    buyer = models.Buyer.objects.create_user(**data)

    tasks.send_verifi_mail_task.delay(
        current_domain=get_current_site(request).domain,
        buyer_id=buyer.id
    )

    return buyer

def buyer_confirm_email(token, uid):
    buyer_id = urlsafe_base64_decode(uid)
    buyer = selectors.get_object(models.Buyer, id=buyer_id)

    if default_token_generator.check_token(buyer, token):
        buyer.is_verified = True
        buyer.save()
        return True
    else:
        raise ValidationError("Link error")


