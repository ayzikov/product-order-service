# installed
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
# local
from apps.orderserviceapi.models import Category
from apps.orderserviceapi.serializers import CategorySerializer


class CategoryListView(APIView):
    def get(self, request: Request):
        """ Получение всех категорий """
        categories = Category.objects.all()
        serializer = CategorySerializer(instance=categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        """ Создание категории """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            category = serializer.save()
            response_data = {"result": "the Category has been created",
                             "Category name": category.name}
            return Response(response_data, status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    def delete(self, request: Request, id: int):
        """ Удаление категории """
        category = get_object_or_404(Category, id=id)
        category_name = category.name
        category.delete()
        data = {"result": f"Category {category_name} deleted"}
        return Response(data)