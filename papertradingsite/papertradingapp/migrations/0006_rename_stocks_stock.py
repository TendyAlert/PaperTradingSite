# Generated by Django 5.0.4 on 2024-04-17 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('papertradingapp', '0005_remove_userbalance_portfolio_stocks_delete_portfolio'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Stocks',
            new_name='Stock',
        ),
    ]
