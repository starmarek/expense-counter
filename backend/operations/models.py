from django.contrib.auth.models import User
from django.db import models

from backend.bank_statement.models import BankStatement


class Operations(models.Model):
    """
    Operations table storing information about single operation siemanko
    """

    datetime = models.DateTimeField()
    value = models.FloatField(null=True)
    category = models.CharField(max_length=150)
    operation_type = models.CharField(max_length=150)
    isExpense = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_statement = models.ForeignKey(BankStatement, null=True, on_delete=models.SET_NULL, related_name="operation")
