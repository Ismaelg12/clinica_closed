# Generated by Django 2.1 on 2019-01-28 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atendimento', '0002_agendamento_cancelado'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='liberado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='status',
            field=models.CharField(blank=True, choices=[('AG', 'Agendado'), ('AT', 'Atendido'), ('CC', 'Cancelado'), ('DM', 'Desmarcado')], default='AG', max_length=2),
        ),
    ]
