# base
# installed
from django.test import TestCase
# local
from apps.orderserviceapi.models import Buyer


class BuyerModelTest(TestCase):
    def setUp(self):
        """
        Создание buyer
        """
        self.buyer = Buyer(
            username="username",
            password="my_password",
            first_name="first_name",
            last_name="last_name",
            age=25,
            email="test@test.test",
        )

    def test_buyer_model(self):
        """
        Проверка создания buyer
        """
        # сохраняем buyer в БД
        self.buyer.clean_fields()
        self.buyer.save()

        # получаем buyer из БД
        buyer = Buyer.objects.get(first_name="first_name")

        # проверяем сохранение
        self.assertEqual(buyer.age, 25)
        self.assertFalse(buyer.is_verified)