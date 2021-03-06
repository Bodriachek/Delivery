# Generated by Django 3.2.1 on 2022-05-12 16:24

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0011_auto_20220512_1828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='car',
            name='deadline',
        ),
        migrations.RemoveField(
            model_name='car',
            name='what_repair',
        ),
        migrations.AlterField(
            model_name='fueling',
            name='date_refueling',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 16, 24, 40, 607527, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_trip',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 16, 24, 40, 607337, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('what_repair', models.CharField(max_length=200)),
                ('deadline', models.DateField(default=datetime.datetime(2022, 5, 12, 16, 24, 40, 607139, tzinfo=utc))),
                ('cost', models.PositiveIntegerField(blank=True, help_text='In UAH', null=True)),
                ('car', models.ForeignKey(blank=True, limit_choices_to=models.Q(('is_repair', True)), null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.car')),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.driver')),
            ],
        ),
    ]
