# base
# installed
from itertools import product

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
# local
from apps.orderserviceapi import db
from apps.orderserviceapi import serializers as app_serializers
from apps.orderserviceapi.models import Product
from apps.orderserviceapi.services import views_adapter
from apps.orderserviceapi.services.errors import get_404_error


class ProductDetailModifyDeleteView(APIView):
    def get(self, request: Request, product_id: int):
        """
        Получение детальной информации
        """
        product = db.product_get(product_id)
        if product is None:
            get_404_error(Product)

        data = app_serializers.ProductOutputDetailSerializer(product).data
        return Response(data, status=status.HTTP_200_OK)


    def patch(self, request: Request, product_id: int):
        """
        Частичное изменение
        """
        serializer = app_serializers.ProductModifySerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        product = views_adapter.product_modify(serializer.validated_data, product_id)
        data = app_serializers.ProductOutputDetailSerializer(product).data
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request: Request, product_id: int):
        """
        Удаление
        """
        views_adapter.product_delete(product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateView(APIView):
    def get(self, request: Request):
        """
        Получение списка
        """
        pass

    def post(self, request: Request):
        """
        Создание
        """
        serializer = app_serializers.ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = views_adapter.product_create(serializer.validated_data)
        data = app_serializers.ProductOutputDetailSerializer(product).data

        return Response(data, status=status.HTTP_201_CREATED)


class ProductStockView(APIView):
    """
    Представление для работы с количеством товара на складе
    """
    def patch(self, request: Request, product_id: int):
        """
        Добавление товара на склад
        """

        serializer = app_serializers.ProductRemainingStockDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = views_adapter.product_remaining_stock_add(serializer.validated_data, product_id)
        data = app_serializers.ProductOutputDetailSerializer(product).data

        return Response(data, status=status.HTTP_200_OK)
