# Generated by Django 5.1.4 on 2024-12-22 12:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0024_alter_trip_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='adult_places',
            field=models.IntegerField(default=None, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='trip',
            name='adult_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='trip',
            name='child_places',
            field=models.IntegerField(default=None, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='trip',
            name='child_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='trip',
            name='duration',
            field=models.IntegerField(default=None, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
