import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from backend.bank_statement.tests.factories import BankStatementFactory
from backend.operations.tests.factories import OperationFactory
from backend.user.tests.factories import UserFactory

register(BankStatementFactory, "bank_statement")
register(OperationFactory, "operation")
register(UserFactory)


@pytest.fixture()
def api_client():
    return APIClient()
