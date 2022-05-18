# Generated by Django 3.2.1 on 2022-05-12 16:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0012_auto_20220512_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fueling',
            name='date_refueling',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 16, 43, 38, 381163, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_trip',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 16, 43, 38, 380981, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='repair',
            name='deadline',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 16, 43, 38, 380769, tzinfo=utc)),
        ),
    ]
