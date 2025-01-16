# Generated by Django 5.1.4 on 2024-12-21 21:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0017_alter_city_continent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='where_from',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='where_from', to='viewer.city'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='where_to',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='where_to', to='viewer.city'),
        ),
    ]