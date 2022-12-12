# Generated by Django 4.1.3 on 2022-11-28 14:12

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apibroker', '0006_alter_case_case_number_alter_case_customer_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='case_file',
            field=models.FileField(blank=True, null=True, upload_to='cases', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xml', 'json'])]),
        ),
        migrations.AlterField(
            model_name='case',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cases', to=settings.AUTH_USER_MODEL, verbose_name='Utilizador'),
        ),
    ]