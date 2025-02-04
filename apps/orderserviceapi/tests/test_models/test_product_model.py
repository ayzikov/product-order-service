# base
# installed
from django.test import TransactionTestCase
# local
from apps.orderserviceapi.models import Product, Provider, Category, RemainingStock


class ProductModelTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        """
        Создание provider, category и product
        """
        self.provider = Provider(
            name="provider1",
            country="country1",
            town="town1",
            street="street1",
            building=1
        )
        self.category = Category(
            name="category1"
        )
        self.product = Product(
            name="product1",
            price=10000,
            provider=self.provider,
            category=self.category
        )
        self.remaining_stock = RemainingStock(
            product=self.product
        )

    def test_product_model(self):
        """
        Проверка создания product и привязки к нему provider и category
        """
        # сохраняем модели в БД
        self.provider.save()
        self.category.save()
        self.product.save()
        self.remaining_stock.save()

        # получаем модели из БД
        provider = Provider.objects.get(name=self.provider.name)
        category = Category.objects.get(name=self.category.name)
        product = Product.objects.get(name=self.product.name)

        # проверка сохраненного product
        self.assertEqual(product.name, "product1")
        self.assertEqual(product.provider, provider)
        self.assertEqual(product.category, category)
        self.assertEqual(product.remainingstock.quantity, 0)