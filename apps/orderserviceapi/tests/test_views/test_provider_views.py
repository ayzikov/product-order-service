# base
# installed
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
# local
from apps.orderserviceapi.models import Provider
from apps.orderserviceapi.services.tests import ProviderFactory


class ProviderViewsTest(APITestCase):
    def setUp(self):
        self.url = reverse("orderserviceapi:providers:list_create")

    def test_provider_create_get_list(self):
        for id in range(1, 3):
            self.provider = ProviderFactory.build()
            self.response_post = self.client.post(
                path=self.url,
                data={
                    "name": self.provider.name,
                    "country": self.provider.country,
                    "town": self.provider.town,
                    "street": self.provider.street,
                    "building": self.provider.building
                }
            )
            # проверка статуса ответа
            self.assertEqual(status.HTTP_201_CREATED, self.response_post.status_code)
            # проверка полей созданного объекта
            response_get_detail = self.client.get(f"{self.url}{id}")

            self.assertEqual(self.response_post.data.get("name"), response_get_detail.data.get("name"))
            self.assertEqual(self.response_post.data.get("country"), response_get_detail.data.get("country"))
            self.assertEqual(self.response_post.data.get("town"), response_get_detail.data.get("town"))
            self.assertEqual(self.response_post.data.get("street"), response_get_detail.data.get("street"))
            self.assertEqual(self.response_post.data.get("building"), response_get_detail.data.get("building"))

        response_get_list = self.client.get(self.url)
        # проверка создания 2-х объектов
        self.assertEqual(len(response_get_list.data), 2)

        # проверка изменения объекта
        self.client.patch(
            f"{self.url}1",
            data={"name": "modified_name"}
        )
        modified_provider = Provider.objects.get(id=1)
        self.assertEqual(modified_provider.name, "modified_name")

        # проверка удаления объекта
        self.client.delete(f"{self.url}1")
        self.assertEqual(Provider.objects.all().count(), 1)




# python manage.py test apps.orderserviceapi.tests.test_views.test_provider_views.ProviderViewsTest