# Generated by Django 5.0.4 on 2024-04-16 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_ticker', models.CharField(max_length=4)),
                ('quantity', models.IntegerField(default=0)),
                ('buy', models.BooleanField(default=False)),
                ('stock_value', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='UserBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(max_length=70)),
                ('last_name', models.TextField(max_length=70)),
                ('balance', models.DecimalField(decimal_places=2, default=2000.0, max_digits=9)),
                ('actions', models.JSONField(default=dict)),
            ],
        ),
    ]
