# base
# installed
from rest_framework import serializers
# local
from apps.orderserviceapi import models
from apps.orderserviceapi import db


# PROVIDER
class ProviderOutputDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        exclude = ["id"]


class ProviderOutputListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = "__all__"


class ProviderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = "__all__"


class ProviderModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        exclude = ["id"]


# BUYER
class BuyerOutputDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Buyer
        fields = ["id", "username", "first_name", "last_name", "age", "email"]


class BuyerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Buyer
        exclude = ["groups", "user_permissions"]


# PRODUCT
class ProductOutputDetailSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ["name", "price", "provider", "category", "quantity"]

    def get_quantity(self, obj):
        """
        Получаем количество товара на складе для вывода в ответе
        """
        return db.product_remaining_stock_get(obj.id).quantity


class ProductOutputListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class ProductModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        exclude = ["id"]


class ProductRemainingStockDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RemainingStock
        fields = ["quantity"]