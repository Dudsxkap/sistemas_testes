import pandas as pd

from django.core.management import BaseCommand

from agendamentos.models import LocalVacinacao


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            print("Iniciando importação do CSV, por favor aguarde...")
            ubs = pd.read_csv("agendamentos/csv_importacao/ubs.csv")
            ubs.apply(
                lambda x: LocalVacinacao.objects.update_or_create(
                    defaults={"nome": x["nom_estab"], "logradouro": x["dsc_endereco"], "bairro": x["dsc_bairro"],
                              "cidade": x["dsc_cidade"]}, cnes=x["cod_cnes"]),
                axis=1)
            print("Importação concluída!")
        except FileNotFoundError:
            print("Arquivo CSV não encontrado, certifique-se de colocar o arquivo CSV no diretório correto.")
        except Exception as e:
            print(f"Ocorreu um erro do tipo: {e}, tente novamente.")
