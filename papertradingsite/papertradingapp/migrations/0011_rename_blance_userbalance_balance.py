# Generated by Django 5.0.4 on 2024-04-19 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('papertradingapp', '0010_rename_stock_value_stock_bought_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbalance',
            old_name='blance',
            new_name='balance',
        ),
    ]