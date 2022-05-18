# Generated by Django 3.2.1 on 2022-05-16 12:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0017_auto_20220514_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_trip',
            field=models.DateField(default=datetime.datetime(2022, 5, 16, 12, 22, 38, 856235, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='repair',
            name='deadline',
            field=models.DateField(default=datetime.datetime(2022, 5, 16, 12, 22, 38, 855980, tzinfo=utc)),
        ),
    ]