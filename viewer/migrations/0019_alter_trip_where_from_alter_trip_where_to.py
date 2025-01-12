# Generated by Django 5.1.4 on 2024-12-21 21:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0018_alter_trip_where_from_alter_trip_where_to'),
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
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='where_to', to='viewer.city'),
        ),
    ]
