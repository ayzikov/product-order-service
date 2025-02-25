# base
# installed
import factory
from faker import Faker
from factory.django import DjangoModelFactory
# local
from apps.orderserviceapi import models


fake = Faker()


class ProviderFactory(DjangoModelFactory):
    name = factory.LazyFunction(lambda: fake.company())
    country = factory.LazyFunction(lambda: fake.country())
    town = factory.LazyFunction(lambda: fake.city())
    street = factory.LazyFunction(lambda: fake.street_name())
    building = factory.LazyFunction(lambda: fake.building_number())

    class Meta:
        model = models.Provider


class BuyerFactory(DjangoModelFactory):
    username = factory.LazyFunction(lambda: fake.user_name())
    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    age = factory.LazyFunction(lambda: fake.random_int(min=18, max=90))
    email = "ayzikov070@yandex.ru"
    password = "mypassword99118822"

    class Meta:
        model = models.Buyer


class CategoryFactory(DjangoModelFactory):
    name = factory.LazyFunction(lambda: fake.name())
    parent = factory.SubFactory(
        'apps.orderserviceapi.services.tests.CategoryFactory',
        parent=None  # по умолчанию создаем корневую категорию
    )

    # установка родителя при создании категории
    @factory.post_generation
    def set_parent(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.parent = extracted
            self.save()

    class Meta:
        model = models.Category


class ProductFactory(DjangoModelFactory):
    name = factory.LazyFunction(lambda: fake.file_name())
    price = factory.LazyFunction(lambda: fake.random_int(min=1000, max=100000))
    provider = factory.SubFactory("apps.orderserviceapi.services.tests.ProviderFactory")
    category = factory.SubFactory("apps.orderserviceapi.services.tests.CategoryFactory")

    class Meta:
        model = models.Product


class OrderFactory(DjangoModelFactory):
    buyer = factory.SubFactory("apps.orderserviceapi.services.tests.BuyerFactory")

    class Meta:
        model = models.Order
