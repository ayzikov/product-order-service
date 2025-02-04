# base
# installed
from django.test import TransactionTestCase
# local
from apps.orderserviceapi.models import Order, Buyer, Product, ProductOrder, Provider, RemainingStock, Category


class OrderModelTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        """
        Создание необходимых моделей для теста
        """
        self.buyer = Buyer(
            username="username1",
            password="my_password1",
            first_name="first_name1",
            last_name="last_name1",
            age=25,
            email="test@test.test1",
        )
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
        self.product1 = Product(
            name="product1",
            price=10000,
            provider=self.provider,
            category=self.category
        )
        self.product2 = Product(
            name="product2",
            price=10000,
            provider=self.provider,
            category=self.category
        )
        self.remaining_stock1 = RemainingStock(
            product=self.product1
        )
        self.remaining_stock2 = RemainingStock(
            product=self.product2
        )
        self.order = Order(
            buyer=self.buyer
        )
        self.product_order1 = ProductOrder(
            quantity=10,
            purchase_price=1000,
            order=self.order,
            product=self.product1
        )
        self.product_order2 = ProductOrder(
            quantity=10,
            purchase_price=1000,
            order=self.order,
            product=self.product2
        )

    def test_order_model(self):
        """
        Проверка создания order и product_order
        """
        # сохраняем модели в БД
        self.buyer.save()
        self.provider.save()
        self.category.save()
        self.product1.save()
        self.product2.save()
        self.remaining_stock1.save()
        self.remaining_stock2.save()
        self.order.save()
        self.product_order1.save()
        self.product_order2.save()

        # получаем модели из БД
        order = Order.objects.get(buyer=self.buyer)

        # проверяем сохранение
        self.assertEqual(order.productorder_set.get(product=self.product1).product.name, "product1")
        self.assertEqual(order.productorder_set.get(product=self.product2).product.name, "product2")