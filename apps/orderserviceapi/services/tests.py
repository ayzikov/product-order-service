# base
# installed
import factory
from faker import Faker
from factory.django import DjangoModelFactory
# local
from apps.orderserviceapi import models


fake = Faker()


class ProviderFactory(DjangoModelFactory):
    name = fake.company() 
    country = fake.country() 
    town = fake.city() 
    street = fake.street_name() 
    building = fake.building_number()

    class Meta:
        model = models.Provider


class BuyerFactory(DjangoModelFactory):
    username = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    age = fake.random_int(min=18, max=90)
    email = "ayzikov070@yandex.ru"
    password = "mypassword99118822"

    class Meta:
        model = models.Buyer


class CategoryFactory(DjangoModelFactory):
    name = fake.name()
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
    name = fake.file_name()
    price = fake.random_int(min=1000, max=100000)
    provider = factory.SubFactory("apps.orderserviceapi.services.tests.ProviderFactory")
    category = factory.SubFactory("apps.orderserviceapi.services.tests.CategoryFactory")

    class Meta:
        model = models.Product