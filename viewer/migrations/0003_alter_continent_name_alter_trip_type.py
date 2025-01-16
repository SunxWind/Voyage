# Generated by Django 5.1.4 on 2024-12-16 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0002_remove_trip_name_alter_trip_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='continent',
            name='name',
            field=models.CharField(choices=[('North America', '------'), ('Africa', 'Africa'), ('Antarctica', 'Antarctica'), ('Asia', 'Asia'), ('Europe', 'Europe'), ('North America', 'North America'), ('Australia & Oceania', 'Australia & Oceania'), ('South America', 'South America')], default='North America', max_length=20),
        ),
        migrations.AlterField(
            model_name='trip',
            name='type',
            field=models.CharField(choices=[('--', '--'), ('BB', 'BB'), ('HB', 'HB'), ('FB', 'FB'), ('AI', 'AI')], default=None, max_length=20),
        ),
    ]