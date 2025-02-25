# base
# installed
from rest_framework import serializers
# local
from apps.orderserviceapi import models
from apps.orderserviceapi import selectors


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
        """ Получаем количество товара на складе для вывода в ответе """
        return selectors.product_remaining_stock_get(obj.id).quantity


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


# ORDER
class OrderOutputDetailSerializer(serializers.ModelSerializer):
    products_order = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        fields = ["buyer", "datetime", "products_order"]

    def get_products_order(self, obj):
        products_order_list = selectors.products_in_order_get_list(order_id=obj.id)
        return [ProductOrderOutputDetailSerializer(product_order).data for product_order in products_order_list]


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ["buyer"]


class ProductOrderOutputDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductOrder
        fields = ["quantity", "purchase_price", "product"]


class OrderAddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductOrder
        fields = ["quantity"]