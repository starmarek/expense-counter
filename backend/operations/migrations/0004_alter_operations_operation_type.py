# Generated by Django 3.2.6 on 2021-08-11 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0003_auto_20210811_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operations',
            name='operation_type',
            field=models.CharField(blank=True, choices=[('ZAKUP PRZY U¯YCIU KARTY', 'ZAKUP PRZY U¯YCIU KARTY'), ('P£ATNO„Æ WEB - KOD MOBILNY', 'P£ATNO„Æ WEB - KOD MOBILNY'), ('PRZELEW WYCHODZ¥CY', 'PRZELEW WYCHODZ¥CY'), ('PRZELEW PRZYCHODZ¥CY', 'PRZELEW PRZYCHODZ¥CY'), ('PRZELEW NA TELEFON PRZYCHODZ. ZEW.', 'PRZELEW NA TELEFON PRZYCHODZ. ZEW.'), ('PRZELEW NA TELEFON WYCHODZ¥CY ZEW.', 'PRZELEW NA TELEFON WYCHODZ¥CY ZEW.'), ('PRZELEW PRZYCH. SYSTEMAT. WP£YW', 'PRZELEW PRZYCH. SYSTEMAT. WP£YW'), ('WYP£ATA W BANKOMACIE', 'WYP£ATA W BANKOMACIE'), ('WP£ATA GOTÓWKI WE WP£ATOMACIE', 'WP£ATA GOTÓWKI WE WP£ATOMACIE')], max_length=150),
        ),
    ]
