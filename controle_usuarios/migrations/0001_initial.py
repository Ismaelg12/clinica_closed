# Generated by Django 2.1 on 2020-07-28 23:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.PositiveSmallIntegerField(choices=[(1, 'Atendente'), (2, 'Fisioterapeuta'), (3, 'Terapeuta ocupacional'), (4, 'Fonoaudiólogo(a)'), (5, 'Psiquiatra'), (6, 'Nutricionista'), (7, 'Psicólogo(a)'), (8, 'Dentista'), (9, 'Educador(a) Físico(a)'), (10, 'Esteticista'), (11, 'Musicoterapeuta'), (12, 'Enfermeiro(a)'), (13, 'Psicopedagogo(a)')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profissional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('sobrenome', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('telefone', models.CharField(blank=True, max_length=15)),
                ('registro', models.CharField(blank=True, max_length=16)),
                ('cpf', models.CharField(max_length=14, null=True, unique=True)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('tipo', models.PositiveSmallIntegerField(choices=[(1, 'Atendente'), (2, 'Profissional')], null=True, verbose_name='Tipo (Permissão)')),
                ('quantidade_atend', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True)),
                ('data_cadastro', models.DateField(auto_now_add=True)),
                ('horario_trabalho', models.CharField(blank=True, max_length=12, verbose_name='Dias de Trabalho')),
                ('ativo', models.BooleanField(default=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('atent_categoria', models.CharField(blank=True, max_length=200, verbose_name='Tipos de atendimentos')),
                ('abordagem', models.CharField(blank=True, max_length=200, verbose_name='Abordagens')),
                ('observacao', models.CharField(blank=True, max_length=200, verbose_name='Outras Observações')),
                ('conta_banco', models.TextField(blank=True, verbose_name='Contas bancarias')),
                ('area_atuacao', models.ManyToManyField(to='controle_usuarios.Perfil')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profissional',
                'verbose_name_plural': 'Profissionais',
            },
        ),
    ]
