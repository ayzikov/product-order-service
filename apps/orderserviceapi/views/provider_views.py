# installed
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
# local
from apps.orderserviceapi.models import Provider
from apps.orderserviceapi.serializers import ProviderSerializer


class ProviderListView(APIView):
    def get(self, request: Request):
        """ Получение всех поставщиков """
        providers = Provider.objects.all()
        serializer = ProviderSerializer(instance=providers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        """ Создание поставщика """
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            provider = serializer.save()
            response_data = {"result": "the provider has been created",
                             "provider name": provider.name}
            return Response(response_data, status=status.HTTP_201_CREATED)


class ProviderDetailView(APIView):
    def get(self, request: Request, id: int):
        """ Получение поставщика """
        provider = get_object_or_404(Provider, id=id)
        serializer = ProviderSerializer(instance=provider)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, id: int):
        """ Обновление поставщика """
        provider = get_object_or_404(Provider, id=id)
        serializer = ProviderSerializer(instance=provider, data=request.data)
        if serializer.is_valid(raise_exception=True):
            provider = serializer.save()
            response_data = {"result": "the provider has been updated",
                             "provider name": provider.name}
            return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request: Request, id: int):
        """ Частичное обновление поставщика """
        provider = get_object_or_404(Provider, id=id)
        serializer = ProviderSerializer(instance=provider, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            provider = serializer.save()
            response_data = {"result": "the provider has been updated",
                             "provider name": provider.name}
            return Response(response_data, status=status.HTTP_200_OK)

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
