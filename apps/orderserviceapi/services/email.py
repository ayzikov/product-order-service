# installed
from typing import Tuple, Any

from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
# local
from apps.orderserviceapi.models import Buyer


def get_activation_url(current_domain, buyer_id) -> tuple[str, str]:
    buyer = get_object_or_404(Buyer, id=buyer_id)
    token = default_token_generator.make_token(buyer)
    uid = urlsafe_base64_encode(force_bytes(buyer.id))

    path = reverse("orderserviceapi:buyers:confirm_email", args=[token, uid])
    return f"http://{current_domain}{path}", buyer.email

def send_verifi_mail(current_domain, buyer_id) -> None:
    # Отправляет письмо на почту при регистрации
    try:
        activation_url, buyer_email = get_activation_url(current_domain, buyer_id)
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты:\n'
            f'{activation_url}',
            settings.EMAIL_HOST_USER,
            [buyer_email],
            fail_silently=False,
        )
    except Exception:
        raise Exception('Ошибка в функции send_verifi_mail')

def send_order_mail(buyer_id) -> None:
    # Отправляет письмо на почту при создании заказа
    try:
        buyer = get_object_or_404(Buyer, id=buyer_id)
        send_mail(
            'Уведомление о создании заказа',
            f'Создан заказ',
            settings.EMAIL_HOST_USER,
            [buyer.email],
            fail_silently=False,
        )
    except Exception:
        raise Exception('Ошибка в функции send_order_mail')