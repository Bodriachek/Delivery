# Generated by Django 3.2.1 on 2022-05-29 09:32

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0030_auto_20220522_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='fueling',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fueling', to='delivery.driver'),
        ),
        migrations.AlterField(
            model_name='car',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='delivery.driver'),
        ),
        migrations.AlterField(
            model_name='car',
            name='tank_size',
            field=models.PositiveSmallIntegerField(help_text='In liters'),
        ),
        migrations.AlterField(
            model_name='fueling',
            name='amount_fuel',
            field=models.PositiveSmallIntegerField(help_text='In liters'),
        ),
        migrations.AlterField(
            model_name='fueling',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fueling', to='delivery.car'),
        ),
        migrations.AlterField(
            model_name='fueling',
            name='fuel_check',
            field=models.ImageField(blank=True, null=True, upload_to='checks/'),
        ),
        migrations.AlterField(
            model_name='order',
            name='car',
            field=models.ForeignKey(limit_choices_to=models.Q(('is_repair', False)), null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='delivery.car'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_trip',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 29, 9, 32, 32, 32698, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='delivery.driver'),
        ),
        migrations.AlterField(
            model_name='order',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='delivery.manager'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_distance',
            field=models.DecimalField(decimal_places=2, help_text='In kilometers', max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='repair',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 29, 9, 32, 32, 32508, tzinfo=utc)),
        ),
    ]