# Generated by Django 3.2.3 on 2021-05-29 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agendamentos',
            options={'ordering': ['status'], 'verbose_name': 'Agendamentos Feitos', 'verbose_name_plural': 'Agendamentos Feitos'},
        ),
        migrations.AlterModelOptions(
            name='localvacinacao',
            options={'ordering': ['cidade', 'bairro', 'logradouro', 'nome'], 'verbose_name': 'Locais de Vacinação', 'verbose_name_plural': 'Locais de Vacinação'},
        ),
        migrations.AlterField(
            model_name='salasagendamento',
            name='numero_vagas',
            field=models.IntegerField(verbose_name='Número de Vagas'),
        ),
    ]