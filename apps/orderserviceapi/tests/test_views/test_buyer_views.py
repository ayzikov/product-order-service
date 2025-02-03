# base
# installed
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APITestCase
# local
from apps.orderserviceapi.models import Buyer
from apps.orderserviceapi.services.tests import BuyerFactory


class BuyerViewsTest(APITestCase):
    def setUp(self):
        self.register_url = reverse("orderserviceapi:buyers:register")
        self.buyer = BuyerFactory.build()

    def test_buyer_views(self):
        # проверка создания объекта
        self.client.post(
            self.register_url,
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

        # проверка перехода по ссылке подтверждения email
        token = default_token_generator.make_token(buyer)
        uid = urlsafe_base64_encode(force_bytes(buyer.id))

        activation_url = reverse("orderserviceapi:buyers:confirm_email", args=[token, uid])
        self.client.get(activation_url)

        buyer = Buyer.objects.get(id=1)
        self.assertTrue(buyer.is_verified)


# python manage.py test apps.orderserviceapi.tests.test_views.test_buyer_views.BuyerViewsTest