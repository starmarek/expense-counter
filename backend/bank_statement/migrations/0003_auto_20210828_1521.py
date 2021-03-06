# Generated by Django 3.2.6 on 2021-08-28 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_statement', '0002_bankstatement_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bankstatement',
            old_name='notes',
            new_name='note',
        ),
        migrations.AddField(
            model_name='bankstatement',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='backend/bank_statement/store/'),
        ),
    ]
