# Generated by Django 3.2.2 on 2021-05-23 05:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0017_alter_order_order_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_data',
            field=models.DateField(default=datetime.datetime(2021, 5, 23, 5, 13, 46, 82337, tzinfo=utc), verbose_name='Дата получения заказа'),
        ),
    ]
