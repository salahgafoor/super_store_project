# Generated by Django 3.1.4 on 2021-01-17 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210117_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='accounts.OrderItem'),
        ),
    ]
