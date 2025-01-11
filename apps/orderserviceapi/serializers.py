# installed
from rest_framework.serializers import ModelSerializer
# local
from apps.orderserviceapi.models import Provider, Product


class ProviderSerializer(ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"