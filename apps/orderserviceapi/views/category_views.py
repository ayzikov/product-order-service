# base
# installed
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
# local
from apps.orderserviceapi.services import db
from apps.orderserviceapi import serializers as app_serializers


class CategoryCreateView(APIView):
    def post(self, request: Request):
        """ Создание """

        serializer = app_serializers.CategoryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = db.category_create(serializer.validated_data)
        data = app_serializers.CategoryOutputDetailSerializer(category).data

        return Response(data, status=status.HTTP_201_CREATED)