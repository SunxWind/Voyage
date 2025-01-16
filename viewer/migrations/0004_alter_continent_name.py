# Generated by Django 5.1.4 on 2024-12-16 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0003_alter_continent_name_alter_trip_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='continent',
            name='name',
            field=models.CharField(choices=[('------', '------'), ('Africa', 'Africa'), ('Antarctica', 'Antarctica'), ('Asia', 'Asia'), ('Europe', 'Europe'), ('North America', 'North America'), ('Australia & Oceania', 'Australia & Oceania'), ('South America', 'South America')], default='North America', max_length=20),
        ),
    ]