# installed
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (extend_schema,
                                   inline_serializer)
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
# local
from apps.orderserviceapi.models import Provider
from apps.orderserviceapi.serializers import ProviderSerializer


class ProviderListView(APIView):
    # GET
    @extend_schema(
        parameters=[],
        tags=["Provider"],
        summary='Все поставщики',
        description=''
    )
    def get(self, request: Request):
        """ Получение всех поставщиков """
        providers = Provider.objects.all()
        serializer = ProviderSerializer(instance=providers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST
    @extend_schema(
        request=inline_serializer(
            name="ProviderPOSTSerializer",
            fields={
                "name": serializers.CharField(default='name'),
                "country": serializers.CharField(default='country'),
                "town": serializers.CharField(default='town'),
                "street": serializers.CharField(default='street'),
                "building": serializers.IntegerField(default='building'),
            },
        ),
        tags=["Provider"],
        summary='Создание поставщика',
        description='',
    )
    def post(self, request: Request):
        """ Создание поставщика """
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            provider = serializer.save()
            response_data = {"result": "the provider has been created",
                             "provider name": provider.name}
            return Response(response_data, status=status.HTTP_201_CREATED)


class ProviderDetailView(APIView):
    # GET
    @extend_schema(
        parameters=[],
        tags=["Provider"],
        summary='Получение поставщика',
        description=''
    )
    def get(self, request: Request, id: int):
        """ Получение поставщика """
        provider = get_object_or_404(Provider, id=id)
        serializer = ProviderSerializer(instance=provider)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST
    @extend_schema(
        request=inline_serializer(
            name="ProviderPUTSerializer",
            fields={
                "name": serializers.CharField(default='name'),
                "country": serializers.CharField(default='country'),
                "town": serializers.CharField(default='town'),
                "street": serializers.CharField(default='street'),
                "building": serializers.IntegerField(default='building'),
            },
        ),
        tags=["Provider"],
        summary='Обновление поставщика',
        description='',
    )
    def put(self, request: Request, id: int):
        """ Обновление поставщика """
        provider = get_object_or_404(Provider, id=id)
        serializer = ProviderSerializer(instance=provider, data=request.data)
        if serializer.is_valid(raise_exception=True):
            provider = serializer.save()
            response_data = {"result": "the provider has been updated",
                             "provider name": provider.name}
            return Response(response_data, status=status.HTTP_200_OK)

    # PATCH
    @extend_schema(
        request=inline_serializer(
            name="ProviderPATCHSerializer",
            fields={
                "town": serializers.CharField(default='town'),
            },
        ),
        tags=["Provider"],
        summary='Частичное обновление поставщика',
        description='',
    )
    def patch(self, request: Request, id: int):
        """ Частичное обновление поставщика """
        provider = get_object_or_404(Provider, id=id)
        serializer = ProviderSerializer(instance=provider, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            provider = serializer.save()
            response_data = {"result": "the provider has been updated",
                             "provider name": provider.name}
            return Response(response_data, status=status.HTTP_200_OK)

    # DELETE
    @extend_schema(
        parameters=[],
        tags=["Provider"],
        summary='Удаление поставщика',
        description=''
    )
    def delete(self, request: Request, id: int):
        """ Удаление поставщика """
        provider = get_object_or_404(Provider, id=id)
        provider_name = provider.name
        provider.delete()
        data = {"result": f"Provider {provider_name} deleted"}
        return Response(data)


# class ProviderViewSet(ModelViewSet):
#     queryset = Provider.objects.all()
#     serializer_class = ProviderSerializer
