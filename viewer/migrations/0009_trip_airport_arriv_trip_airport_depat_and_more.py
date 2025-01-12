# Generated by Django 5.1.4 on 2024-12-19 22:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0008_alter_trip_where_from_alter_trip_where_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='airport_arriv',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='airport_arriv', to='viewer.airport'),
        ),
        migrations.AddField(
            model_name='trip',
            name='airport_depat',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='airport_depat', to='viewer.airport'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='where_to',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='where_to', to='viewer.city'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='where_to_hotel',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='viewer.hotel'),
        ),
    ]
