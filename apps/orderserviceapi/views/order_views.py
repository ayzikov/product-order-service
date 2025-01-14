# installed
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
# local
from apps.orderserviceapi.models import Order, ProductOrder
from apps.orderserviceapi.serializers import OrderSerializer


class OrderView(APIView):
    def get(self, request: Request):
        """ Получение всех заказов """
        orders = Order.objects.all()
        serializer = OrderSerializer(instance=orders, context={'request': request.data}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        """ Создание заказа """
        serializer = OrderSerializer(data=request.data, context={'request': request.data})
        if serializer.is_valid(raise_exception=True):
            order = serializer.save()
            response_data = {"result": "the order has been created"}
            return Response(response_data, status=status.HTTP_201_CREATED)