# installed
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
# local
from apps.orderserviceapi.models import Buyer
from apps.orderserviceapi.serializers import BuyerSerializer
from services.tasks import send_verifi_mail_task


class BuyerView(APIView):
    def get(self, request: Request):
        """ Получение всех поставщиков """
        buyers = Buyer.objects.all()
        serializer = BuyerSerializer(instance=buyers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        """ Регистрация пользователя """
        serializer = BuyerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            buyer = serializer.save()
            current_domain = get_current_site(request).domain
            send_verifi_mail_task.delay(current_domain, buyer.id)
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