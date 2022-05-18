# Generated by Django 3.2.1 on 2022-05-12 08:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_auto_20220511_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_trip',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 8, 54, 56, 211040, tzinfo=utc), verbose_name='Дата доставки'),
        ),
        migrations.AlterField(
            model_name='registrationrefueling',
            name='date_refueling',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 8, 54, 56, 211254, tzinfo=utc), verbose_name='Дата заправки'),
        ),
    ]
