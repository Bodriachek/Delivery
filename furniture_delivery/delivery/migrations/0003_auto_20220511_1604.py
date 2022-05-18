# Generated by Django 3.2.1 on 2022-05-11 13:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_auto_20220511_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_trip',
            field=models.DateField(default=datetime.datetime(2022, 5, 11, 13, 4, 41, 130860, tzinfo=utc), verbose_name='Дата доставки'),
        ),
        migrations.AlterField(
            model_name='registrationrefueling',
            name='date_refueling',
            field=models.DateField(default=datetime.datetime(2022, 5, 11, 13, 4, 41, 131126, tzinfo=utc), verbose_name='Дата заправки'),
        ),
    ]