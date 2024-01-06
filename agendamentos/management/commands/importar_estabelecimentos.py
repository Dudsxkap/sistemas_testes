from django.core.management.base import BaseCommand
from agendamentos.models import EstabelecimentoSaude
import xml.etree.ElementTree as ET
import os


class Command(BaseCommand):
    help = 'Importa arquivo xml com estabelecimentos'

    def handle(self, *args, **options):
        try:
            path = os.path.join('agendamentos', 'management', 'xml_importacao', 'estabelecimentos_saude.xml', )
            estabelecimentos_save = []
            xml_data = open(path, 'r').read()
            estabelecimentos = ET.XML(xml_data)
            for estabelecimento in estabelecimentos:
                estabelecimentos_save.append(
                    EstabelecimentoSaude(
                        nome=estabelecimento.find('no_fantasia').text,
                        cnes=estabelecimento.find('co_cnes').text
                    )
                )

            EstabelecimentoSaude.objects.bulk_create(estabelecimentos_save)

            print("Estabelecimentos importados com sucesso!")
        except Exception as e:
            print(e)
