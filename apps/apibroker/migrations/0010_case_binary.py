# Generated by Django 4.1.3 on 2022-12-02 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apibroker', '0009_case_preshared_key_alter_case_case_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='binary',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
