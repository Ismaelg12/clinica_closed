# Generated by Django 2.1 on 2019-02-06 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convenio',
            name='nome',
            field=models.CharField(choices=[('particular', 'Particular'), ('unimed', 'Unimed'), ('humanasaude', 'Humana Saúde'), ('saudecaixa', 'Saúde Caixa'), ('intermed', 'Intermed'), ('geapsaude', 'Geap Saúde'), ('fumsa', 'Fusma'), ('cassi', 'Cassi')], max_length=40),
        ),
    ]