# Generated by Django 3.2.3 on 2021-06-01 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0004_alter_user_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salasagendamento',
            name='id_agendamento_disponivel',
        ),
        migrations.RemoveField(
            model_name='salasagendamento',
            name='id_sala',
        ),
        migrations.RenameField(
            model_name='agendamentos',
            old_name='id_agendamento_disponivel',
            new_name='agendamento_disponivel',
        ),
        migrations.RenameField(
            model_name='agendamentos',
            old_name='id_cidadao',
            new_name='cidadao',
        ),
        migrations.RenameField(
            model_name='agendamentos',
            old_name='id_grupo',
            new_name='grupo',
        ),
        migrations.RenameField(
            model_name='agendamentosdisponiveis',
            old_name='id_vacina',
            new_name='vacina',
        ),
        migrations.AddField(
            model_name='agendamentosdisponiveis',
            name='local_vacinacao',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='agendamentos.localvacinacao', verbose_name='Local de vacinação'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agendamentosdisponiveis',
            name='num_vagas',
            field=models.IntegerField(default=0, verbose_name='Número de vagas'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Sala',
        ),
        migrations.DeleteModel(
            name='SalasAgendamento',
        ),
    ]