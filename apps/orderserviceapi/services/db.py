# base
# installed
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
# local
from apps.orderserviceapi import selectors
from apps.orderserviceapi import models
from apps.orderserviceapi.services import errors, tasks


# PROVIDER
def provider_create(data: dict) -> models.Provider:
    """ Создание поставщика """
    provider = models.Provider.objects.create(**data)
    return provider


def provider_modify(provider_id: int, data: dict) -> models.Provider:
    """ Изменение поставщика """
    models.Provider.objects.filter(id=provider_id).update(**data)
    return selectors.provider_get(provider_id)


def provider_delete(provider_id: int) -> None:
    """ Удаление поставщика """
    provider = selectors.provider_get(provider_id)
    if provider is None:
        errors.get_404_error(models.Provider)
    provider.delete()


# BUYER
def buyer_create(request: Request, data: dict) -> models.Buyer:
    """ Создание покупателя """
    buyer = models.Buyer.objects.create_user(**data)
    # запуск таски на отправку письма подтверждения
    tasks.send_verifi_mail_task.delay(
        current_domain=get_current_site(request).domain,
        buyer_id=buyer.id
    )

    return buyer


def buyer_confirm_email(token, uid) -> bool | None:
    """ Подтверждение email """
    buyer_id = urlsafe_base64_decode(uid)
    buyer = selectors.buyer_get(buyer_id)

    if default_token_generator.check_token(buyer, token):
        buyer.is_verified = True
        buyer.save()
        return True
    else:
        raise ValidationError("Link error")


# PRODUCT
def product_create(data: dict) -> models.Product:
    """ Создание товара """
    product = models.Product.objects.create(**data)
    remaining_stock_create(product.id)

    return product


def remaining_stock_create(product_id: int) -> models.RemainingStock:
    """ Создание remaining stock """
    remaining_stock = models.RemainingStock.objects.create(product_id=product_id)
    return remaining_stock


def product_modify(data: dict, product_id: int) -> models.Product:
    """ Изменение товара """
    models.Product.objects.filter(id=product_id).update(**data)
    return selectors.product_get(product_id)


def product_remaining_stock_add(quantity: int, product_id: int) -> models.Product:
    """ Добавление товара на склад """
    remaining_stock = selectors.product_remaining_stock_get(product_id)
    remaining_stock.quantity += quantity
    remaining_stock.save()

    product = selectors.product_get(product_id)
    return product


def product_remaining_stock_reduce(data: dict, product_id: int) -> models.Product:
    """ Убрать товар со склада """
    remaining_stock = selectors.product_remaining_stock_get(product_id)
    remaining_stock.quantity -= data.get("quantity")
    remaining_stock.save()

    product = selectors.product_get(product_id)
    return product


def product_delete(product_id: int) -> None:
    """ Удаление товара """
    product = selectors.product_get(product_id)
    if product is None:
        errors.get_404_error(models.Product)
    product.delete()


# ORDER
def order_create(data: dict) -> models.Order:
    """ Создание заказа """
    order = models.Order.objects.create(**data)

    # отправка email покупателю
    tasks.send_order_mail_task.delay(
        buyer_id=data.get("buyer").id
    )

    return order


def product_in_order_create(data: dict, order_id: int, product_id: int) -> models.ProductOrder:
    """ Создание ProductInOrder """
    # получение остатка товара на складе и товар
    product = selectors.product_get(product_id)
    product_remaining_stock = selectors.product_remaining_stock_get(product_id)
    # проверка на количество товара
    quantity = data.get("quantity")
    if product_remaining_stock.quantity < quantity:
        # вызываем ошибку
        errors.get_product_order_quantity_error()

    # при добавлении товара в заказ вычитаем количество товара на складе
    product_remaining_stock_reduce(data, product_id)

    # создаем ProductOrder
    product_order = models.ProductOrder.objects.create(
        quantity=quantity,
        purchase_price=product.price,
        order_id=order_id,
        product_id=product_id
    )
    return product_order


def order_confirm(order_id: int) -> None:
    """ Подтверждение заказа """
    order = selectors.order_get(order_id)
    order.delete()


def order_cancel(order_id: int) -> None:
    """ Отмена заказа """
    # возвращаем количество товара на склад
    #   - получаем список товаров, которые находятся в заказе
    #   - берем количество товара из заказа и добавляем его к количеству товара на складе
    #     с помощью функции product_remaining_stock_add
    products_in_order_list = selectors.products_in_order_get_list(order_id)
    for product_in_order in products_in_order_list:
        product_id = product_in_order.product.id
        quantity = product_in_order.quantity
        product_remaining_stock_add(quantity, product_id)

    # удаляем заказ
    order = selectors.order_get(order_id)
    order.delete()


# CATEGORY
def category_create(data: dict) -> models.Category:
    category = models.Category.objects.create(**data)
    return category