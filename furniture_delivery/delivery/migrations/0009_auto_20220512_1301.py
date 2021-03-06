# Generated by Django 3.2.1 on 2022-05-12 10:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0008_auto_20220512_1301'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registrationrefueling',
            options={},
        ),
        migrations.AlterField(
            model_name='order',
            name='date_trip',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 10, 1, 47, 323708, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='registrationrefueling',
            name='date_refueling',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 10, 1, 47, 323907, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='registrationrefueling',
            name='price',
            field=models.FloatField(help_text='In UAH', null=True),
        ),
    ]
