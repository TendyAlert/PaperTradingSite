# Generated by Django 5.0.4 on 2024-04-21 01:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papertradingapp', '0013_transactionhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionhistory',
            name='transaction_date',
            field=models.IntegerField(default=datetime.datetime(2024, 4, 20, 20, 16, 31, 416588)),
        ),
    ]
