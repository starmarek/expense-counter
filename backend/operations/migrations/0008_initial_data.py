from django.core.management import call_command
from django.db import migrations


def forwards_func(apps, schema_editor):
    call_command("loaddata", r"fixtures\fixtures.json")


class Migration(migrations.Migration):
    dependencies = [
        ("operations", "0007_auto_20210917_1749"),
    ]
    operations = [migrations.RunPython(forwards_func)]
