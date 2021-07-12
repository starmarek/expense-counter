from django.contrib.auth.models import User
from django.db import models


class Operations(models.Model):
    """
    Operations table storing information about single operation siemanko
    """

    datetime = models.DateTimeField()
    category = models.CharField(max_length=150)
    operation_type = models.CharField(max_length=150)
    isExpense = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
