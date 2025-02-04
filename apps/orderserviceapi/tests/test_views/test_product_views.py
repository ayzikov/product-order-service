# base
# installed
from django.urls import reverse
from rest_framework.test import APITransactionTestCase
from rest_framework import status
# local
from apps.orderserviceapi.models import Product, RemainingStock
from apps.orderserviceapi.services.tests import ProductFactory


class ProductViewsTest(APITransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.url_list_create = reverse("orderserviceapi:products:list_create")
        self.url_detail_modify_delete = reverse("orderserviceapi:products:detail_modify_delete", args=[1])
        self.url_stock = reverse("orderserviceapi:products:stock", args=[1])
        self.product = ProductFactory().build()

    def test_product_views(self):
        # ПРОВЕРКА СОЗДАНИЯ ТОВАРА
        response_post = self.client.post(
            path=self.url_list_create,
            data={
                "name": self.product.name,
                "price": self.product.price,
                "provider": self.product.provider,
                "category": self.product.category,
            }
        )
        # проверяем код ответа
        self.assertEqual(status.HTTP_201_CREATED, response_post.status_code)
        # проверяем получение объекта из БД по эндпоинту
        response_detail = self.client.get(self.url_detail_modify_delete)
        self.assertEqual(self.product.name, response_detail.data.get("name"))
        self.assertEqual(self.product.price, response_detail.data.get("price"))
        self.assertEqual(self.product.provider, response_detail.data.get("provider"))
        self.assertEqual(self.product.category, response_detail.data.get("category"))

        # ПРОВЕРКА ИЗМЕНЕНИЯ ТОВАРА
        self.client.patch(
            path=self.url_detail_modify_delete,
            data={
                "name": "modified_name"
            }
        )
        self.product = Product.objects.get(id=1)
        self.assertEqual(self.product.name, "modified_name")

        # ПРОВЕРКА ДОБАВЛЕНИЯ ТОВАРА НА СКЛАД
        self.client.patch(
            path=self.url_stock,
            data={
                "quantity": 5
            }
        )
        # получаю RemainingStock, который должен создаться вместе с товаром
        # и проверяю количество
        self.remaining_stock = RemainingStock.objects.get(product=self.product)
        self.assertEqual(5, self.remaining_stock.quantity)

        # ПРОВЕРКА УДАЛЕНИЯ ТОВАРА
        self.client.delete(self.url_detail_modify_delete)
        self.assertFalse(Product.objects.all().exists())
        self.assertFalse(RemainingStock.objects.all().exists())


# python manage.py test apps.orderserviceapi.tests.test_views.test_product_views.ProductViewsTest