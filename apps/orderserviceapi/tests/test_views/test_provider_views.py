# base
# installed
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITransactionTestCase
# local
from apps.orderserviceapi.models import Provider
from apps.orderserviceapi.services.tests import ProviderFactory


class ProviderViewsTest(APITransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.url_list_create = reverse("orderserviceapi:providers:list_create")
        self.url_get_modify_delete = reverse("orderserviceapi:providers:detail_modify_delete", args=[1])

    def test_provider_views(self):
        # проверка создания объекта
        for id in range(1, 3):
            provider = ProviderFactory.build()
            response_post = self.client.post(
                path=self.url_list_create,
                data={
                    "name": provider.name,
                    "country": provider.country,
                    "town": provider.town,
                    "street": provider.street,
                    "building": provider.building
                }
            )
            # проверка статуса ответа
            self.assertEqual(status.HTTP_201_CREATED, response_post.status_code)
            # проверка полей созданного объекта
            self.url_detail = reverse("orderserviceapi:providers:detail_modify_delete", args=[id])
            response_get_detail = self.client.get(self.url_detail)

            self.assertEqual(response_post.data.get("name"), response_get_detail.data.get("name"))
            self.assertEqual(response_post.data.get("country"), response_get_detail.data.get("country"))
            self.assertEqual(response_post.data.get("town"), response_get_detail.data.get("town"))
            self.assertEqual(response_post.data.get("street"), response_get_detail.data.get("street"))
            self.assertEqual(response_post.data.get("building"), response_get_detail.data.get("building"))

        # проверка создания 2-х объектов
        response_get_list = self.client.get(self.url_list_create)
        self.assertEqual(len(response_get_list.data), 2)

        # проверка изменения объекта
        self.client.patch(self.url_get_modify_delete, data={"name": "modified_name"})
        modified_provider = Provider.objects.get(id=1)
        self.assertEqual(modified_provider.name, "modified_name")

        # проверка удаления объекта
        self.client.delete(self.url_get_modify_delete)
        self.assertEqual(Provider.objects.all().count(), 1)




# python manage.py test apps.orderserviceapi.tests.test_views.test_provider_views.ProviderViewsTest