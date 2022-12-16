# Generated by Django 4.1.4 on 2022-12-16 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apibroker', '0016_caseinstancemanager_customer_id_usercase_customer_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='caseinstancemanager',
            old_name='case_number',
            new_name='caseNumber',
        ),
        migrations.RenameField(
            model_name='caseinstancemanager',
            old_name='customer_id',
            new_name='customerId',
        ),
        migrations.RenameField(
            model_name='caseinstancemanager',
            old_name='ext_reference_nr',
            new_name='extReferenceNumber',
        ),
        migrations.RenameField(
            model_name='caseinstancemanager',
            old_name='operator_id',
            new_name='operatorId',
        ),
        migrations.RenameField(
            model_name='caseinstancemanager',
            old_name='origin_id',
            new_name='originId',
        ),
        migrations.RenameField(
            model_name='caseinstancemanager',
            old_name='plate_number',
            new_name='plateNumber',
        ),
        migrations.RenameField(
            model_name='usercase',
            old_name='customer_id',
            new_name='customerId',
        ),
        migrations.RenameField(
            model_name='usercase',
            old_name='operator_id',
            new_name='operatorId',
        ),
        migrations.RenameField(
            model_name='usercase',
            old_name='origin_id',
            new_name='originId',
        ),
    ]