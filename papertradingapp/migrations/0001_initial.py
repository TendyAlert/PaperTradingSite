# Generated by Django 5.0.4 on 2024-04-17 21:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_balance', models.DecimalField(decimal_places=2, default=2000.0, max_digits=9)),
                ('stock_ticker', models.CharField(max_length=4)),
                ('quantity', models.IntegerField(default=0)),
                ('stock_value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('buy', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
