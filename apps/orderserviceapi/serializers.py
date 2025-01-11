# installed
from rest_framework.serializers import ModelSerializer
# local
from apps.orderserviceapi.models import Provider, Product, Category, RemainingStock


class ProviderSerializer(ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class RemainingStockSerializer(ModelSerializer):
    class Meta:
        model = RemainingStock
        fields = ["quantity"]