# Generated by Django 3.2.6 on 2021-08-28 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_statement', '0003_auto_20210828_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankstatement',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='api/bank_statement/store/'),
        ),
    ]
