from django.core.management.base import BaseCommand
from agendamentos.models import GrupoAtendimento
import xml.etree.ElementTree as ET
import os


class Command(BaseCommand):
    help = 'Importa arquivo xml com grupos de atendimentos'

    def handle(self, *args, **options):
        try:
            path = os.path.join('agendamentos', 'management', 'xml_importacao', 'grupos_atendimento.xml', )
            grupos_save = []
            xml_data = open(path, 'r').read()
            grupos = ET.XML(xml_data)
            for grupo in grupos:
                grupos_save.append(
                    GrupoAtendimento(
                        nome=grupo.find('nome').text,
                        codigo_si_pni=grupo.find('codigo_si_pni').text
                    )
                )

            GrupoAtendimento.objects.bulk_create(grupos_save)

            print("Grupos importados com sucesso!")
        except Exception as e:
            print(e)
