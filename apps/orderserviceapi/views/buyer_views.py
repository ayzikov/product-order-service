# base
# installed
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
# local
from apps.orderserviceapi import serializers as app_serializers
from apps.orderserviceapi.models import Buyer
from apps.orderserviceapi.services import db


class BuyerRegisterView(APIView):
    def post(self, request: Request):
        """
        Регистрация
        """

        serializer = app_serializers.BuyerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        buyer = db.buyer_create(request, serializer.validated_data)

        data = app_serializers.BuyerOutputDetailSerializer(buyer).data

        return Response(data, status=status.HTTP_201_CREATED)


class BuyerConfirmEmailView(APIView):
    def get(self, request: Request, token: str, uid: str):
        """
        Подтверждение email
        """

        db.buyer_confirm_email(token, uid)

        return Response(status=status.HTTP_204_NO_CONTENT)