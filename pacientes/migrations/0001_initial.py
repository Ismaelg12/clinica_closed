# Generated by Django 2.2.5 on 2019-09-27 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('controle_usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60, verbose_name='Nome')),
                ('pai', models.CharField(blank=True, max_length=60)),
                ('mae', models.CharField(blank=True, max_length=60)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('sexo', models.CharField(blank=True, choices=[('F', 'Feminino'), ('M', 'Masculino')], max_length=1, verbose_name='Sexo')),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('rg', models.CharField(blank=True, max_length=14, null=True)),
                ('uf', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MT', 'Mato Grosso'), ('MA', 'Maranhão'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RO', 'Rondônia'), ('RS', 'Rio Grande do Sul'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SE', 'Sergipe'), ('SP', 'São Paulo'), ('TO', 'Tocantins')], default='PI', max_length=2)),
                ('possui_cpf', models.BooleanField(default=False)),
                ('cidade', models.CharField(blank=True, max_length=40, verbose_name='Cidade')),
                ('rua', models.CharField(blank=True, max_length=70, verbose_name='Rua')),
                ('bairro', models.CharField(blank=True, max_length=70, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=70)),
                ('cep', models.CharField(blank=True, max_length=12, verbose_name='CEP')),
                ('email', models.EmailField(blank=True, max_length=70, null=True, verbose_name='E-mail')),
                ('telefone', models.CharField(max_length=20, verbose_name='Telefone Principal')),
                ('telefone_fixo', models.CharField(blank=True, max_length=20, verbose_name='Telefone Fixo')),
                ('raca', models.CharField(blank=True, choices=[('B', 'Branca'), ('P', 'Preta'), ('D', 'Parda'), ('A', 'Amarela'), ('I', 'Indigena')], max_length=1)),
                ('estado_civil', models.CharField(blank=True, choices=[('', 'Escolha Um Opçao'), ('S', 'Solteiro'), ('C', 'Casado'), ('D', 'Divorciado'), ('V', 'Viúvo'), ('U', 'União Estável')], max_length=1)),
                ('profissao', models.CharField(blank=True, max_length=50)),
                ('num_convenio', models.CharField(blank=True, max_length=17, verbose_name='Nº da Carteira')),
                ('validade_carteira', models.DateField(blank=True, null=True, verbose_name='Validade Carteira')),
                ('observacao', models.TextField(blank=True, max_length=500)),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('convenio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Convenio')),
                ('profissional', models.ManyToManyField(to='controle_usuarios.Profissional')),
            ],
            options={
                'verbose_name_plural': 'pacientes',
                'ordering': ['nome'],
                'verbose_name': 'paciente',
            },
        ),
    ]
