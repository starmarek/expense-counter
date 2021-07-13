from django.contrib.auth.models import User
from django.db import models


class BankStatement(models.Model):
    notes = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
