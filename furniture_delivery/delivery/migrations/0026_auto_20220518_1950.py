# Generated by Django 3.2.1 on 2022-05-18 16:50

import datetime
import denorm.fields
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0025_auto_20220518_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='all_mileage',
            field=denorm.fields.CountField('total_mileage', default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_trip',
            field=models.DateField(default=datetime.datetime(2022, 5, 18, 16, 50, 40, 323137, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='repair',
            name='deadline',
            field=models.DateField(default=datetime.datetime(2022, 5, 18, 16, 50, 40, 322934, tzinfo=utc)),
        ),
    ]
