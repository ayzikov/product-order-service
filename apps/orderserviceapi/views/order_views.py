# base
# installed
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
# local
from apps.orderserviceapi import selectors
from apps.orderserviceapi import serializers as app_serializers
from apps.orderserviceapi.models import Order
from apps.orderserviceapi.services.errors import get_404_error
from apps.orderserviceapi.services import db


class OrderDetailModifyDeleteView(APIView):
    def get(self, request: Request, order_id: int):
        """ Получение детальной информации """

        order = selectors.order_get(order_id)
        if order is None:
            get_404_error(Order)
        data = app_serializers.OrderOutputDetailSerializer(order).data

        return Response(data, status=status.HTTP_200_OK)


class OrderListCreateView(APIView):
    def get(self, request: Request):
        """ Получение списка """

        pass

    def post(self, request: Request):
        """ Создание """

        serializer = app_serializers.OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = db.order_create(serializer.validated_data)
        data = app_serializers.OrderOutputDetailSerializer(order).data

        return Response(data, status=status.HTTP_201_CREATED)


class OrderAddProductView(APIView):
    def post(self, request: Request, order_id: int, product_id: int):
        """ Добавление товара в заказ """

        serializer = app_serializers.OrderAddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_order = db.product_in_order_create(serializer.validated_data, order_id, product_id)
        data = app_serializers.ProductOrderOutputDetailSerializer(product_order).data

        return Response(data, status=status.HTTP_201_CREATED)


class OrderConfirmView(APIView):
    """ Подтверждение """

    def post(self, request: Request, order_id: int):
        db.order_confirm(order_id)

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderCancelView(APIView):
    """ Отмена """

    def post(self, request: Request, order_id: int):
        db.order_cancel(order_id)

        return Response(status=status.HTTP_204_NO_CONTENT)
