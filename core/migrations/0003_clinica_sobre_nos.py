# Generated by Django 3.0.3 on 2020-08-08 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200808_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinica',
            name='sobre_nos',
            field=models.TextField(blank=True, max_length=400),
        ),
    ]