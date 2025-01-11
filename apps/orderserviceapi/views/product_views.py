# installed
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
# local
from apps.orderserviceapi.models import Product, RemainingStock
from apps.orderserviceapi.serializers import ProductSerializer, RemainingStockSerializer


class ProductListView(APIView):
    def get(self, request: Request):
        """ Получение всех товаров """
        products = Product.objects.all()
        serializer = ProductSerializer(instance=products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

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
    def get(self, request: Request, id: int):
        """ Получение товара """
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(instance=product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, id: int):
        """ Обновление товара """
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid(raise_exception=True):
            product = serializer.save()
            response_data = {"result": "the Product has been updated",
                             "Product name": product.name}
            return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request: Request, id: int):
        """ Частичное обновление товара """
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            product = serializer.save()
            response_data = {"result": "the Product has been updated",
                             "Product name": product.name}
            return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request: Request, id: int):
        """ Удаление товара """
        product = get_object_or_404(Product, id=id)
        product_name = product.name
        product.delete()
        data = {"result": f"Product {product_name} deleted"}
        return Response(data)


class ProductWarehouseView(APIView):
    def get(self, request: Request, id: int):
        """ Остаток товара на складе """
        product = get_object_or_404(Product, id=id)
        remaining_stock = RemainingStock.objects.get(product=product)
        response_data = {f"Количество {product.name} на складе = {remaining_stock.quantity}"}
        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request: Request, id: int):
        """ Добавить товар на склад """
        product = get_object_or_404(Product, id=id)
        remaining_stock = RemainingStock.objects.get(product=product)
        serializer = RemainingStockSerializer(instance=remaining_stock, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            remaining_stock = serializer.save()
            response_data = {f"Количество {product.name} изменено на {remaining_stock.quantity}"}
            return Response(response_data, status=status.HTTP_200_OK)