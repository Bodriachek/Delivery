# Generated by Django 3.2.1 on 2022-05-22 15:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0029_auto_20220522_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_trip',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 22, 15, 56, 57, 237311, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='repair',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 22, 15, 56, 57, 237122, tzinfo=utc)),
        ),
    ]
