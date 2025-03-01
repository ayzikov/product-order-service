# base
# installed
from django.http import Http404
from rest_framework.exceptions import ValidationError
# local


def get_404_error(model):
    raise Http404(f"{model._meta.object_name} не найден в БД")


def get_product_order_quantity_error():
    raise ValidationError("Невозможно добавить товара в заказ больше чем есть на складе")