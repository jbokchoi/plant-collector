# Generated by Django 2.2 on 2019-06-10 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='humidity',
            field=models.CharField(default='Any humidity will do!', max_length=100),
        ),
        migrations.AddField(
            model_name='plant',
            name='light',
            field=models.CharField(default='Medium indirect light', max_length=100),
        ),
        migrations.AddField(
            model_name='plant',
            name='water',
            field=models.CharField(default='When soil is dry', max_length=100),
        ),
    ]
