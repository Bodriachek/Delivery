# Generated by Django 3.2.1 on 2022-05-11 13:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_auto_20220511_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='mileage',
        ),
        migrations.AlterField(
            model_name='order',
            name='date_trip',
            field=models.DateField(default=datetime.datetime(2022, 5, 11, 13, 49, 56, 502173, tzinfo=utc), verbose_name='Дата доставки'),
        ),
        migrations.AlterField(
            model_name='registrationrefueling',
            name='date_refueling',
            field=models.DateField(default=datetime.datetime(2022, 5, 11, 13, 49, 56, 502384, tzinfo=utc), verbose_name='Дата заправки'),
        ),
    ]
