# base
# installed
from faker import Faker
from factory.django import DjangoModelFactory
# local
from apps.orderserviceapi.models import Provider


fake = Faker()


class ProviderFactory(DjangoModelFactory):
    name = fake.company() 
    country = fake.country() 
    town = fake.city() 
    street = fake.street_name() 
    building = fake.building_number()

    class Meta:
        model = Provider