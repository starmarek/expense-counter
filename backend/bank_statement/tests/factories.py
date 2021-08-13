from datetime import date

import factory

from ...user.tests.factories import UserFactory
from ..models import BankStatement


class BankStatementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BankStatement

    user = factory.SubFactory(UserFactory)
    notes = "tmp"
    date = date.today()
