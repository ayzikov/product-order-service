# base
# installed
from django.urls import reverse
from rest_framework.test import APITransactionTestCase
from rest_framework import status
# local
from apps.orderserviceapi import selectors
from apps.orderserviceapi.services import db
from apps.orderserviceapi.services.tests import ProductFactory, BuyerFactory

from apps.orderserviceapi import models


class OrderViewsTest(APITransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.product = ProductFactory()
        # добавляем количество товара
        db.remaining_stock_create(self.product.id)
        db.product_remaining_stock_add(10, self.product.id)

        self.buyer_1 = BuyerFactory()
        self.buyer_2 = BuyerFactory(email="test@mail.ru")

        self.url_list_create = reverse("orderserviceapi:orders:list_create")
        self.url_detail_modify_delete = reverse("orderserviceapi:orders:detail_modify_delete", args=[1])
        self.url_confirm = reverse("orderserviceapi:orders:confirm", args=[1])
        self.url_cancel = reverse("orderserviceapi:orders:cancel", args=[2])

        self.url_add_product_in_order_1 = reverse("orderserviceapi:orders:add_product", args=[1, 1])
        self.url_add_product_in_order_2 = reverse("orderserviceapi:orders:add_product", args=[2, 1])


    def test_order_views(self):
        # ПРОВЕРКА СОЗДАНИЯ ЗАКАЗА
        # создаем 2 заказа
        response_post_1 = self.client.post(
            path=self.url_list_create,
            data={
                "buyer": self.buyer_1.id
            }
        )
        response_post_2 = self.client.post(
            path=self.url_list_create,
            data={
                "buyer": self.buyer_2.id
            }
        )

        self.assertEqual(status.HTTP_201_CREATED, response_post_1.status_code)
        self.assertEqual(status.HTTP_201_CREATED, response_post_2.status_code)

        # проверяем эндпоинт получения информации о заказе
        response_detail = self.client.get(self.url_detail_modify_delete)
        self.assertEqual(self.buyer_1.id, response_detail.data.get("buyer"))

        # ПРОВЕРКА ДОБАВЛЕНИЯ ТОВАРА В ЗАКАЗ
        # добавляем товар в первый заказ и проверяем что количество товара на складе изменилось и создался ProductOrder
        response_add_product_1 = self.client.post(
            path=self.url_add_product_in_order_1,
            data={
                "quantity": 6
            }
        )
        self.assertEqual(response_add_product_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, models.ProductOrder.objects.all().count())

        product_remaining_stock = selectors.product_remaining_stock_get(self.product.id)
        self.assertEqual(product_remaining_stock.quantity, 4)

        # добавляем в заказ больше товара чем есть на складе и проверяем что сервис выдал ошибку
        response_add_product_2 = self.client.post(
            path=self.url_add_product_in_order_1,
            data={
                "quantity": 6
            }
        )
        self.assertEqual(response_add_product_2.status_code, status.HTTP_400_BAD_REQUEST)

        # добавляем товар во второй заказ
        response_add_product_3 = self.client.post(
            path=self.url_add_product_in_order_2,
            data={
                "quantity": 4
            }
        )
        self.assertEqual(response_add_product_3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, models.ProductOrder.objects.all().count())

        product_remaining_stock = selectors.product_remaining_stock_get(self.product.id)
        self.assertEqual(product_remaining_stock.quantity, 0)

        # ПРОВЕРКА ПОДТВЕРЖДЕНИЯ ЗАКАЗА
        # подтверждаем первым покупателем и проверяем что заказ был удален
        response_confirm = self.client.post(self.url_confirm)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response_confirm.status_code)
        self.assertIsNone(selectors.order_get(order_id=1))
        self.assertIsNone(selectors.product_in_order_get(order_id=1, product_id=1))

        # ПРОВЕРКА ОТМЕНЫ ЗАКАЗА
        # отменяем, проверяем что заказ был удален и количество товара из заказа вернулось на склад
        response_cancel = self.client.post(self.url_cancel)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response_cancel.status_code)
        self.assertIsNone(selectors.order_get(order_id=2))


        product_remaining_stock = selectors.product_remaining_stock_get(self.product.id)
        self.assertEqual(product_remaining_stock.quantity, 4)


# python manage.py test apps.orderserviceapi.tests.test_views.test_order_views.OrderViewsTest