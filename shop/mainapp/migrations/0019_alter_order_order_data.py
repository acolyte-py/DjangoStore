# Generated by Django 3.2.2 on 2021-05-23 05:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_alter_order_order_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_data',
            field=models.DateField(default=datetime.datetime(2021, 5, 23, 5, 18, 17, 63130, tzinfo=utc), verbose_name='Дата получения заказа'),
        ),
    ]
