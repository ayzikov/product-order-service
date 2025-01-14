# installed
from http.client import HTTPException

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
# local
from apps.orderserviceapi.models import Provider, Product, Category, RemainingStock, Buyer, Order, ProductOrder
from services.tasks import send_order_mail_task


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

    def update(self, instance, validated_data):
        instance.quantity += validated_data.get('quantity')
        instance.save()
        return instance


class BuyerSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = Buyer
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'is_verified']
        read_only_fields = ['id']


class ProductOrderSerializer(ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = "__all__"


class OrderSerializer(ModelSerializer):
    product_order = SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'datetime', 'buyer', 'product_order']

    def create(self, validated_data):
        # данные с запроса
        quantity = self.context['request']['quantity']
        product_id = self.context['request']['product']
        buyer = validated_data.get("buyer", None)

        # проверяем есть ли такое количество товара как пришло в запросе
        product = get_object_or_404(Product, id=product_id)
        remaining_stock = RemainingStock.objects.get(product=product)
        if remaining_stock.quantity < quantity:
            raise Exception("На складе нет такого количества товара")

        buyer = get_object_or_404(Buyer, id=buyer.id)
        # создаем заказ
        order = Order.objects.create(buyer=buyer)
        # создаем товар в заказе
        product_order = ProductOrder.objects.create(
            quantity=quantity,
            purchase_price=product.price,
            order=order,
            product=product
        )
        # меняем количество товара на складе
        remaining_stock.quantity -= quantity
        remaining_stock.save()

        # отправляем покупателю письмо о создании заказа
        send_order_mail_task(buyer.id)

        return order

    def get_product_order(self, obj):
        queryset = ProductOrder.objects.filter(order=obj)
        request = self.context.get('request', None)
        return [ProductOrderSerializer(q, context={'request': request}).data for q in queryset]

