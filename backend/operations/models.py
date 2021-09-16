from django.contrib.auth.models import User
from django.db import models

from backend.bank_statement.models import BankStatement


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Operations(models.Model):
    """
    Operations table storing information about single operation
    """

    CHOICES = [
        ("ZAKUP PRZY UŻYCIU KARTY", "ZAKUP PRZY UŻYCIU KARTY"),
        ("PŁATNOŚĆ WEB - KOD MOBILNY", "PŁATNOŚĆ WEB - KOD MOBILNY"),
        ("PRZELEW WYCHODZĄCY", "PRZELEW WYCHODZĄCY"),
        ("PRZELEW PRZYCHODZĄCY", "PRZELEW PRZYCHODZĄCY"),
        ("PRZELEW NA TELEFON PRZYCHODZ. ZEW.", "PRZELEW NA TELEFON PRZYCHODZ. ZEW."),
        ("PRZELEW NA TELEFON WYCHODZĄCY ZEW.", "PRZELEW NA TELEFON WYCHODZĄCY ZEW."),
        ("PRZELEW PRZYCH. SYSTEMAT. WPŁYW", "PRZELEW PRZYCH. SYSTEMAT. WPŁYW"),
        ("WYPŁATA W BANKOMACIE", "WYPŁATA W BANKOMACIE"),
        ("WPŁATA GOTÓWKI WE WPŁATOMACIE", "WPŁATA GOTÓWKI WE WPŁATOMACIE"),
        ("PRZELEW NA TELEFON PRZYCHODZ. WEW.", "PRZELEW NA TELEFON PRZYCHODZ. WEW."),
    ]

    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    value = models.DecimalField(null=True, max_digits=15, decimal_places=2)
    balance = models.DecimalField(null=True, max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    details = models.CharField(max_length=500, blank=True, null=False)
    operation_type = models.CharField(max_length=150, blank=True, null=False, choices=CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_statement = models.ForeignKey(BankStatement, null=True, on_delete=models.CASCADE, related_name="operation")
