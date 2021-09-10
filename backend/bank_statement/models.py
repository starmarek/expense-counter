from django.contrib.auth.models import User
from django.db import models

from backend.settings import STORE_PATH


class BankStatement(models.Model):
    note = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_upload = models.DateField(null=True, unique=False)
    date = models.DateField(null=True, unique=True)
    file = models.FileField(upload_to=STORE_PATH, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
