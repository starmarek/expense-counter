from django.contrib.auth.models import User
from django.db import models

from backend.bank_statement.models import BankStatement


class Operations(models.Model):
    """
    Operations table storing information about single operation siemanko
    """

    CHOICES = [
        ("ZAKUP PRZY U¯YCIU KARTY", "ZAKUP PRZY U¯YCIU KARTY"),
        ("P£ATNO„Æ WEB - KOD MOBILNY", "P£ATNO„Æ WEB - KOD MOBILNY"),
        ("PRZELEW WYCHODZ¥CY", "PRZELEW WYCHODZ¥CY"),
        ("PRZELEW PRZYCHODZ¥CY", "PRZELEW PRZYCHODZ¥CY"),
        ("PRZELEW NA TELEFON PRZYCHODZ. ZEW.", "PRZELEW NA TELEFON PRZYCHODZ. ZEW."),
        ("PRZELEW NA TELEFON WYCHODZ¥CY ZEW.", "PRZELEW NA TELEFON WYCHODZ¥CY ZEW."),
        ("PRZELEW PRZYCH. SYSTEMAT. WP£YW", "PRZELEW PRZYCH. SYSTEMAT. WP£YW"),
        ("WYP£ATA W BANKOMACIE", "WYP£ATA W BANKOMACIE"),
        ("WP£ATA GOTÓWKI WE WP£ATOMACIE", "WP£ATA GOTÓWKI WE WP£ATOMACIE"),
    ]

    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    value = models.DecimalField(null=True, max_digits=15, decimal_places=2)
    balance = models.DecimalField(null=True, max_digits=15, decimal_places=2)
    category = models.CharField(max_length=150, blank=True, null=False)
    details = models.CharField(max_length=500, blank=True, null=False)
    operation_type = models.CharField(max_length=150, blank=True, null=False, choices=CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_statement = models.ForeignKey(BankStatement, null=True, on_delete=models.SET_NULL, related_name="operation")
