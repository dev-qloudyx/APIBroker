# Generated by Django 4.1.4 on 2022-12-16 12:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apibroker', '0014_rename_customer_key_case_operator_id_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Case',
            new_name='CaseInstanceManager',
        ),
    ]
