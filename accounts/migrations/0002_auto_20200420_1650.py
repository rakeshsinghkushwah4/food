# Generated by Django 2.1.4 on 2020-04-20 11:20

import accounts.account_validation
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=100, validators=[accounts.account_validation.validator.name]),
        ),
    ]
