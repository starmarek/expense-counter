from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class Operations(models.Model):
    """
    Operations table storing information about single operation
    """

    datetime = models.DateTimeField()
    category = models.CharField(max_length=150)
    operation_type = models.CharField(max_length=150)
    isExpense = models.BooleanField()
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
