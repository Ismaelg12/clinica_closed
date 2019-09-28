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
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, max_length=200, null=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Categorias',
                'verbose_name': 'Categoria',
            },
        ),
        migrations.CreateModel(
            name='ContaReceber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('valor_inicial', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6)),
                ('valor_pago_dinheiro', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('valor_pago_cartao', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('status', models.CharField(choices=[('PG', 'Pago'), ('PD', 'Pendente'), ('FT', 'Faturado'), ('PC', 'Parcial')], default='PG', max_length=2)),
                ('forma_pagamento', models.CharField(blank=True, choices=[('CV', 'Convênio'), ('DI', 'Dinheiro'), ('CC', 'Cartão de crédito'), ('EC', 'Dinheiro e Cartão'), ('BB', 'Boleto bancário'), ('TB', 'Transferência bancária')], default='CV', max_length=2)),
                ('cartao_credito', models.CharField(blank=True, choices=[('VS', 'Visa'), ('MC', 'Mastercard'), ('AE', 'American Express'), ('EO', 'Elo')], max_length=2)),
                ('receptor', models.CharField(choices=[('PF', 'Profissional'), ('RC', 'Recepção')], max_length=2)),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('agendamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agenda.Agendamento')),
                ('convenio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Convenio')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pacientes.Paciente')),
                ('procedimento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.Procedimento')),
                ('profissional', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='controle_usuarios.Profissional')),
            ],
            options={
                'verbose_name_plural': 'ContasReceber',
                'verbose_name': 'ContaReceber',
            },
        ),
        migrations.CreateModel(
            name='ContaPagar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vencimento', models.DateField(null=True)),
                ('valor_total', models.CharField(max_length=20)),
                ('n_parcela', models.IntegerField(blank=True, choices=[(0, 'Escolha uma opção'), (1, '1x'), (2, '2x'), (3, '3x'), (4, '4x'), (5, '5x'), (6, '6x'), (7, '7x'), (8, '8x'), (9, '9x'), (10, '10x'), (11, '11x'), (12, '12x')], default=1, verbose_name='Nº Da Parcela')),
                ('status_pag', models.BooleanField(default=False)),
                ('forma_pagamento', models.CharField(choices=[('CV', 'Convênio'), ('DI', 'Dinheiro'), ('CC', 'Cartão de crédito'), ('EC', 'Dinheiro e Cartão'), ('BB', 'Boleto bancário'), ('TB', 'Transferência bancária')], max_length=100)),
                ('conta_fixa', models.NullBooleanField(default=False)),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='financeiro.Categoria')),
                ('profissional', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='controle_usuarios.Profissional')),
            ],
            options={
                'verbose_name_plural': 'Contas a pagar',
                'verbose_name': 'Conta a pagar',
            },
        ),
    ]
