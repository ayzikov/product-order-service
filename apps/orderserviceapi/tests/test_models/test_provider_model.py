# installed
from django.test import TransactionTestCase
# local
from apps.orderserviceapi.models import Provider


class ProviderModelTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        """
        Создание 2-х экземпляров модели Provider
        """
        self.provider_1 = Provider(
            name="provider1",
            country="country1",
            town="town1",
            street="street1",
            building=1
        )
        self.provider_2 = Provider(
            name="provider2",
            country="country2",
            town="town2",
            street="street2",
            building=1
        )

    def test_create_provider(self):
        """
        Тестируется сохранене 2-х моделей Provider
        """
        # сохраняем модели в БД
        self.provider_1.save()
        self.provider_2.save()

        # получаем всех providers из БД и проверяем что их 2
        providers_qs = Provider.objects.all()
        self.assertEqual(providers_qs.count(), 2)

        # проверяем сохранение name у providers
        provider_1 = providers_qs[0]
        provider_2 = providers_qs[1]
        self.assertEqual(provider_1.name, "provider1")
        self.assertEqual(provider_2.name, "provider2")

