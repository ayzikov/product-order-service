# installed
from rest_framework.serializers import ModelSerializer, CharField
# local
from apps.orderserviceapi.models import Provider, Product, Category, RemainingStock, Buyer


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


class BuyerSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = Buyer
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'is_verified']
        read_only_fields = ['id']