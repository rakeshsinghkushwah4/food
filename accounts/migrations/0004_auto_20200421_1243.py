# Generated by Django 2.1.4 on 2020-04-21 07:13

import accounts.account_validation
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=100, validators=[accounts.account_validation.validator.phone, django.core.validators.MaxLengthValidator(10)]),
        ),
    ]
