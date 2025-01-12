# installed
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
# local
from apps.orderserviceapi.models import Buyer
from apps.orderserviceapi.serializers import BuyerSerializer


class BuyerView(APIView):
    def get(self, request: Request):
        """ Получение всех поставщиков """
        buyers = Buyer.objects.all()
        serializer = BuyerSerializer(instance=buyers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        """ Регистрация пользователя """
        def send_verifi_mail(buyer: Buyer):
            # Отправляет письмо на почту
            token = default_token_generator.make_token(buyer)
            uid = urlsafe_base64_encode(force_bytes(buyer.id))
            current_site = get_current_site(request).domain
            activation_url = f'http://{current_site}/confirm-email/{token}/{uid}'
            send_mail(
                'Подтвердите свой электронный адрес',
                f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты:\n'
                f'{activation_url}',
                settings.EMAIL_HOST_USER,
                [buyer.email],
                fail_silently=False,
            )

        serializer = BuyerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            buyer = serializer.save()
            send_verifi_mail(buyer)
            response_data = {"result": "the buyer has been register",
                             "buyer email": buyer.email}
            return Response(response_data, status=status.HTTP_201_CREATED)


class BuyerConfirmEmailView(APIView):
    def get(self, request: Request, token, uidb64):
        buyer_id = urlsafe_base64_decode(uidb64)
        buyer = get_object_or_404(Buyer, id=buyer_id)

        if default_token_generator.check_token(buyer, token):
            buyer.is_verified = True
            buyer.save()
            return Response("Почта подтверждена")