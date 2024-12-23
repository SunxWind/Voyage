# Generated by Django 5.1.4 on 2024-12-19 21:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0007_alter_city_country_city_continent_delete_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='where_from',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='where_from', to='viewer.city'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='where_to',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='viewer.city'),
        ),
    ]
