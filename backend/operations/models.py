from django.contrib.auth.models import User
from django.db import models

from backend.bank_statement.models import BankStatement


class Operations(models.Model):
    """
    Operations table storing information about single operation siemanko
    """

    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    value = models.DecimalField(null=True, max_digits=15, decimal_places=2)
    balance = models.DecimalField(null=True, max_digits=15, decimal_places=2)
    category = models.CharField(max_length=150, blank=True, null=False)
    details = models.CharField(max_length=500, blank=True, null=False)
    operation_type = models.CharField(max_length=150, blank=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_statement = models.ForeignKey(BankStatement, null=True, on_delete=models.SET_NULL, related_name="operation")
