from django.contrib.auth.models import User
from django.db import models


class BankStatement(models.Model):
    notes = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # operations = models.ForeignKey(Operations, on_delete=models.CASCADE)
