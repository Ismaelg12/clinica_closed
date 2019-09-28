# Generated by Django 2.2.5 on 2019-09-27 21:43

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('pacientes', '0001_initial'),
        ('controle_usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.DateField(null=True)),
                ('hora_inicio', models.TimeField(null=True)),
                ('hora_fim', models.TimeField(null=True)),
                ('telefone', models.CharField(blank=True, max_length=15)),
                ('observacao', models.TextField(blank=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('status', models.CharField(blank=True, choices=[('AG', 'Agendado'), ('AT', 'Atendido'), ('FJ', 'Justificada'), ('FH', 'Justificada na Hora'), ('FN', 'Não Justificada'), ('DM', 'Desmarcado/Profisssional'), ('CC', 'Cancelado'), ('BQ', 'Bloqueio'), ('PT', 'Particular'), ('AD', 'Atender')], default='AG', max_length=2)),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('cancelado', models.TextField(blank=True, max_length=50)),
                ('liberado', models.BooleanField(default=False)),
                ('valor', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=6, null=True, verbose_name='Valor do Atendimento')),
                ('pago', models.BooleanField(default=False, verbose_name='pagamento')),
                ('pacote', models.BooleanField(default=False, verbose_name='pacote')),
                ('convenio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Convenio')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pacientes.Paciente')),
                ('profissional', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='controle_usuarios.Profissional')),
                ('sala', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Sala')),
            ],
            options={
                'verbose_name_plural': 'Agendamentos',
                'verbose_name': 'Agendamento',
            },
        ),
    ]
