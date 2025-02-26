# base
# installed
from django.urls import reverse
from rest_framework.test import APITransactionTestCase
from rest_framework import status
# local
from apps.orderserviceapi import selectors
from apps.orderserviceapi.services import db


class CategoryViewsTest(APITransactionTestCase):
    reset_sequences = True

    def setUp(self):
        """
        устанавливаем urls
        """
        self.url_create = reverse("orderserviceapi:categories:create")

    def test_category_views(self):
        """
        создаем категории (1)
                          /\
                         2 3
                        /
                       4
        """
        # создание категорий
        response_post_1 = self.client.post(
            path=self.url_create,
            data={"name": "main"}
        )
        response_post_2 = self.client.post(
            path=self.url_create,
            data={"name": "second lvl 1", "parent": 1}
        )
        response_post_3 = self.client.post(
            path=self.url_create,
            data={"name": "second lvl 2", "parent": 1}
        )
        response_post_4 = self.client.post(
            path=self.url_create,
            data={"name": "third lvl 1", "parent": 2}
        )

        # проверяем связи между категориями
        self.assertEqual("main", selectors.category_get(4).parent.parent.name)
        self.assertEqual("main", selectors.category_get(3).parent.name)


# python manage.py test apps.orderserviceapi.tests.test_views.test_category_views.CategoryViewsTest