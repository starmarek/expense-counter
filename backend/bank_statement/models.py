from django.contrib.auth.models import User
from django.db import models

from backend.operations.models import Operations


class BankStatement(models.Model):
    notes = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    operations = models.ForeignKey(Operations, null=True, on_delete=models.CASCADE)
