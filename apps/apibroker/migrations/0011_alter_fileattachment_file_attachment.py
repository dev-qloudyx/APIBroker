# Generated by Django 4.1.3 on 2022-12-02 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apibroker', '0010_case_binary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileattachment',
            name='file_attachment',
            field=models.FileField(blank=True, null=True, upload_to='cases/attachments/'),
        ),
    ]