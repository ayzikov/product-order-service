# base
# installed
from functools import partial

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
# local
from apps.orderserviceapi import serializers as app_serializers
from apps.orderserviceapi.models import Provider
from apps.orderserviceapi.selectors import provider_get, provider_get_list
from apps.orderserviceapi.services.db import provider_create, provider_modify, provider_delete
from apps.orderserviceapi.services.errors import get_404_error


class ProviderDetailModifyDeleteView(APIView):
    def get(self, request: Request, provider_id: int):
        provider = provider_get(provider_id)
        if provider is None:
            get_404_error(Provider)

        data = app_serializers.ProviderOutputDetailSerializer(provider).data
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request: Request, provider_id: int):
        serializer = app_serializers.ProviderModifySerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        modified_provider = provider_modify(provider_id, serializer.validated_data)
        data = app_serializers.ProviderOutputDetailSerializer(modified_provider).data

        return Response(data, status=status.HTTP_200_OK)
    
    def delete(self, request: Request, provider_id: int):
        provider_delete(provider_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProviderListCreateView(APIView):
    def get(self, request: Request):
        providers_qs = provider_get_list()
        data = app_serializers.ProviderOutputListSerializer(providers_qs, many=True).data

        return Response(data, status=status.HTTP_200_OK)

    
    def post(self, request: Request):
        serializer = app_serializers.ProviderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = provider_create(serializer.validated_data)
        data = app_serializers.ProviderOutputDetailSerializer(provider).data

        return Response(data, status=status.HTTP_201_CREATED)
