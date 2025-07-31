import factory
from django.contrib.auth import get_user_model
import random

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    phone = factory.LazyAttribute(
        lambda x: f'1{random.randint(3, 9)}{random.randint(100000000, 999999999)}'
    )
    id_number = factory.LazyAttribute(
        lambda x: f'{random.randint(100000, 999999)}19{random.randint(1000, 9999)}{random.randint(1000, 9999)}'
    )
    is_active = True
    is_staff = False
