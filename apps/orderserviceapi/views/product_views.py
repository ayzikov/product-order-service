# installed
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (extend_schema,
                                   inline_serializer)
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
# local
from apps.orderserviceapi.models import Product, RemainingStock
from apps.orderserviceapi.serializers import ProductSerializer, RemainingStockSerializer


class ProductListView(APIView):
    # GET
    @extend_schema(
        parameters=[],
        tags=["Product"],
        summary='Все товары',
        description=''
    )
    def get(self, request: Request):
        """ Получение всех товаров """
        products = Product.objects.all()
        serializer = ProductSerializer(instance=products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST
    @extend_schema(
        request=inline_serializer(
            name="ProductPOSTSerializer",
            fields={
                "name": serializers.CharField(default='name'),
                "price": serializers.IntegerField(default=1),
                "provider": serializers.IntegerField(default=1),
                "category": serializers.IntegerField(default=1),
            },
        ),
        tags=["Product"],
        summary='Создание товара',
        description='provider - id поставщика, category - id категории',
    )
    def post(self, request: Request):
        """ Создание товара """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            product = serializer.save()
            # создаем связанную с товаром таблицу остатка на складе
            RemainingStock.objects.create(product=product)
            response_data = {"result": "the Product has been created",
                             "Product name": product.name}
            return Response(response_data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    # GET
    @extend_schema(
        parameters=[],
        tags=["Product"],
        summary='Получение товара',
        description=''
    )
    def get(self, request: Request, id: int):
        """ Получение товара """
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(instance=product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT
    @extend_schema(
        request=inline_serializer(
            name="ProductPUTSerializer",
            fields={
                "name": serializers.CharField(default='name'),
                "price": serializers.IntegerField(default=1),
                "provider": serializers.IntegerField(default=1),
                "category": serializers.IntegerField(default=1),
            },
        ),
        tags=["Product"],
        summary='Обновление товара',
        description='provider - id поставщика, category - id категории',
    )
    def put(self, request: Request, id: int):
        """ Обновление товара """
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid(raise_exception=True):
            product = serializer.save()
            response_data = {"result": "the Product has been updated",
                             "Product name": product.name}
            return Response(response_data, status=status.HTTP_200_OK)

    # PUT
    @extend_schema(
        request=inline_serializer(
            name="ProductPATCHSerializer",
            fields={
                "name": serializers.CharField(default='name'),
                "price": serializers.IntegerField(default=1),
            },
        ),
        tags=["Product"],
        summary='Частичное обновление товара',
        description='',
    )
    def patch(self, request: Request, id: int):
        """ Частичное обновление товара """
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            product = serializer.save()
            response_data = {"result": "the Product has been updated",
                             "Product name": product.name}
            return Response(response_data, status=status.HTTP_200_OK)

    # GET
    @extend_schema(
        parameters=[],
        tags=["Product"],
        summary='Удаление товара',
        description=''
    )
    def delete(self, request: Request, id: int):
        """ Удаление товара """
        product = get_object_or_404(Product, id=id)
        product_name = product.name
        product.delete()
        data = {"result": f"Product {product_name} deleted"}
        return Response(data)


class ProductWarehouseView(APIView):
    # GET
    @extend_schema(
        parameters=[],
        tags=["Product Warehouse"],
        summary='Остаток товара на складе',
        description=''
    )
    def get(self, request: Request, id: int):
        """ Остаток товара на складе """
        product = get_object_or_404(Product, id=id)
        remaining_stock = RemainingStock.objects.get(product=product)
        response_data = {f"Количество {product.name} на складе = {remaining_stock.quantity}"}
        return Response(response_data, status=status.HTTP_200_OK)

    # PUT
    @extend_schema(
        request=inline_serializer(
            name="ProductWarehousePUTSerializer",
            fields={
                "quantity": serializers.IntegerField(default=1),
            },
        ),
        tags=["Product Warehouse"],
        summary='Добавление товара на склад',
        description='quantity - количество товара, которое надо добавить на склад',
    )
    def put(self, request: Request, id: int):
        """ Добавить товар на склад """
        product = get_object_or_404(Product, id=id)
        remaining_stock = RemainingStock.objects.get(product=product)
        serializer = RemainingStockSerializer(instance=remaining_stock, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            remaining_stock = serializer.save()
            response_data = {f"Количество {product.name} изменено на {remaining_stock.quantity}"}
            return Response(response_data, status=status.HTTP_200_OK)