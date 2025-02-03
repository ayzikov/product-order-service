# base
# installed
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
# local
from apps.orderserviceapi.models import Buyer
from apps.orderserviceapi.services.tests import BuyerFactory


class BuyerViewsTest(APITestCase):
    def setUp(self):
        self.url = reverse("orderserviceapi:buyers:register")
        self.buyer = BuyerFactory.build()

    def test_buyer_views(self):
        # проверка создания объекта
        self.client.post(
            self.url,
            data={
                "username": self.buyer.username,
                "first_name": self.buyer.first_name,
                "last_name": self.buyer.last_name,
                "email": self.buyer.email,
                "password": self.buyer.password,
                "age": self.buyer.age
            }
        )
        buyer = Buyer.objects.get(id=1)

        self.assertEqual(buyer.username, self.buyer.username)
        self.assertEqual(buyer.first_name, self.buyer.first_name)
        self.assertEqual(buyer.last_name, self.buyer.last_name)
        self.assertEqual(buyer.email, self.buyer.email)
        self.assertEqual(buyer.age, self.buyer.age)

        self.assertNotEqual(buyer.password, self.buyer.password)


# python manage.py test apps.orderserviceapi.tests.test_views.test_buyer_views.BuyerViewsTest