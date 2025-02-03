# base
# installed
from faker import Faker
from factory.django import DjangoModelFactory
# local
from apps.orderserviceapi.models import Provider, Buyer


fake = Faker()


class ProviderFactory(DjangoModelFactory):
    name = fake.company() 
    country = fake.country() 
    town = fake.city() 
    street = fake.street_name() 
    building = fake.building_number()

    class Meta:
        model = Provider


class BuyerFactory(DjangoModelFactory):
    username = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    age = fake.random_int(min=18, max=90)
    email = "ayzikov070@yandex.ru"
    password = "mypassword99118822"

    class Meta:
        model = Buyer