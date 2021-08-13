import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "test"
    first_name = "Tester"
    last_name = "Braun"
