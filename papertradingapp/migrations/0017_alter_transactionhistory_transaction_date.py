# Generated by Django 5.0.4 on 2024-04-21 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papertradingapp', '0016_alter_transactionhistory_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionhistory',
            name='transaction_date',
            field=models.DateTimeField(),
        ),
    ]