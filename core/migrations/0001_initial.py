# Generated by Django 2.1 on 2020-07-28 23:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('controle_usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_menu', models.ImageField(upload_to='media')),
                ('clinica', models.CharField(blank=True, max_length=50)),
                ('cnpj', models.CharField(blank=True, max_length=18)),
                ('endereco', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Clinica ',
                'verbose_name_plural': 'Clinica',
            },
        ),
        migrations.CreateModel(
            name='Convenio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(choices=[('particular', 'Particular'), ('unimed', 'Unimed'), ('intermed', 'Intermed'), ('humanasaude', 'Humana Saúde'), ('geapsaude', 'Geap Saúde'), ('fusma', 'Fusma'), ('cassi', 'Cassi'), ('caixa_economica', 'Caixa Economica'), ('camed', 'Camed'), ('medplan', 'Medplan'), ('petrobras', 'Petrobrás'), ('capsesp', 'Capsesp'), ('bradesco', 'Bradesco'), ('assefaz', 'Assefaz'), ('correios', 'Correios'), ('pro_bomo', 'Pro Bomo')], max_length=40)),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Convenio',
                'verbose_name_plural': 'Convenios',
            },
        ),
        migrations.CreateModel(
            name='ListaEspera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40)),
                ('idade', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('data_nascimento', models.DateField()),
                ('sexo', models.CharField(blank=True, choices=[('F', 'Feminino'), ('M', 'Masculino')], max_length=1, verbose_name='Sexo')),
                ('turno_manha', models.BooleanField(blank=True, default=False)),
                ('turno_tarde', models.BooleanField(blank=True, default=False)),
                ('turno_noite', models.BooleanField(blank=True, default=False)),
                ('especialidade', models.IntegerField(blank=True, choices=[(1, 'Atendente'), (2, 'Fisioterapeuta'), (3, 'Terapeuta ocupacional'), (4, 'Fonoaudiólogo(a)'), (5, 'Psiquiatra'), (6, 'Nutricionista'), (7, 'Psicólogo(a)'), (8, 'Dentista'), (9, 'Educador(a) Físico(a)'), (10, 'Esteticista'), (11, 'Musicoterapeuta'), (12, 'Enfermeiro(a)'), (13, 'Psicopedagogo(a)')], null=True)),
                ('telefone', models.CharField(blank=True, max_length=20, verbose_name='Telefone Principal')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('observacao', models.TextField(blank=True, max_length=200)),
                ('profissional', models.ManyToManyField(to='controle_usuarios.Profissional')),
            ],
            options={
                'verbose_name': 'Lista de Espera',
                'verbose_name_plural': 'Listas de Espera',
            },
        ),
        migrations.CreateModel(
            name='Procedimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20)),
                ('nome', models.CharField(max_length=50)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=6)),
                ('descricao', models.TextField(blank=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('ativo', models.BooleanField(default=True)),
                ('convenio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Convenio')),
            ],
            options={
                'verbose_name': 'Procedimento',
                'verbose_name_plural': 'Procedimentos',
            },
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40)),
                ('descricao', models.TextField(blank=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
            ],
            options={
                'verbose_name': 'Sala',
                'verbose_name_plural': 'Salas',
            },
        ),
    ]
