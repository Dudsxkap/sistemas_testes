from datetime import datetime, timedelta, time

from django.core.management.base import BaseCommand
from agendamentos.models import EstabelecimentoSaude, AgendamentoDisponivel


class Command(BaseCommand):
    help = 'Importa arquivo xml com estabelecimentos'

    def add_arguments(self, parser):
        parser.add_argument('data_inicial', type=str)
        parser.add_argument('data_final', type=str)

    def handle(self, *args, **options):
        try:
            data_inicial = datetime.strptime(options['data_inicial'], "%Y-%m-%d").date()
            data_final = datetime.strptime(options['data_final'], "%Y-%m-%d").date()
            save_agendamentos = []
            parametros = [
                {
                    "horario": time(13, 0),
                    "idade_inicial": 18,
                    "idade_final": 29
                },
                {
                    "horario": time(14, 0),
                    "idade_inicial": 30,
                    "idade_final": 39
                },
                {
                    "horario": time(15, 0),
                    "idade_inicial": 40,
                    "idade_final": 49
                },
                {
                    "horario": time(16, 0),
                    "idade_inicial": 50,
                    "idade_final": 59
                },
                {
                    "horario": time(17, 0),
                    "idade_inicial": 60,
                    "idade_final": 150
                }
            ]

            while True:
                if data_inicial.weekday() in [2, 3, 4, 5]:
                    for estabelecimento in EstabelecimentoSaude.objects.all():
                        for parametro in parametros:
                            agendamento = AgendamentoDisponivel(
                                data=datetime.combine(data_inicial, parametro["horario"]),
                                num_vagas=5,
                                idade_inicial=parametro["idade_inicial"],
                                idade_final=parametro["idade_final"],
                                estabelecimento_saude=estabelecimento
                            )
                            save_agendamentos.append(agendamento)

                if data_inicial == data_final:
                    break
                data_inicial = data_inicial + timedelta(days=1)
            AgendamentoDisponivel.objects.bulk_create(save_agendamentos)
        except Exception as e:
            print(e)
