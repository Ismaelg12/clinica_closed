# Generated by Django 3.1.7 on 2021-05-03 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atendimento', '0003_auto_20210323_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avaliacao',
            name='condulta',
            field=models.TextField(blank=True, max_length=400, verbose_name='Condulta'),
        ),
        migrations.AlterField(
            model_name='avaliacao',
            name='familia',
            field=models.TextField(blank=True, max_length=400, verbose_name='Histórico Familiar'),
        ),
        migrations.AlterField(
            model_name='avaliacao',
            name='patologico',
            field=models.TextField(blank=True, max_length=400, verbose_name='Histórico Patológico'),
        ),
        migrations.AlterField(
            model_name='avaliacao',
            name='queixa',
            field=models.TextField(blank=True, max_length=400, verbose_name='Queixa Principal'),
        ),
        migrations.AlterField(
            model_name='avaliacao',
            name='social',
            field=models.TextField(blank=True, max_length=400, verbose_name='HIstórico Social'),
        ),
    ]
