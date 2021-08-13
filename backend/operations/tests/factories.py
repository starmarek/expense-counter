from datetime import datetime

import factory

from ...bank_statement.tests.factories import BankStatementFactory
from ..models import Operations


class OperationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Operations

    bank_statement = factory.SubFactory(BankStatementFactory)
    date = datetime.now().date()
    time = datetime.now().time()
    user = factory.SelfAttribute("bank_statement.user")
    value = 69.00
    balance = 1000.00
    operation_type = "PRZELEW WYCHODZĄCY"
    details = "zakupy w biedronce"
