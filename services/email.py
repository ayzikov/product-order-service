# installed
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
# local
from apps.orderserviceapi.models import Buyer


def send_verifi_mail(current_domain, buyer_id):
    # Отправляет письмо на почту
    try:
        buyer = get_object_or_404(Buyer, id=buyer_id)
        token = default_token_generator.make_token(buyer)
        uid = urlsafe_base64_encode(force_bytes(buyer.id))
        activation_url = f'http://{current_domain}/confirm-email/{token}/{uid}'
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты:\n'
            f'{activation_url}',
            settings.EMAIL_HOST_USER,
            [buyer.email],
            fail_silently=False,
        )
    except Exception:
        raise Exception('Ошибка в функции send_verifi_mail')