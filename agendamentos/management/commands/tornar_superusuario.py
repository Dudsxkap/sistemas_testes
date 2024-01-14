from datetime import datetime, timedelta, time

from django.core.management.base import BaseCommand
from agendamentos.models import User


class Command(BaseCommand):
    help = 'Torna um usuário em superusuário'

    def add_arguments(self, parser):
        parser.add_argument('cpf', type=str)

    def handle(self, *args, **options):
        try:
            user = User.objects.get(cpf=options['cpf'])
            user.is_staff = True
            user.save()
        except Exception as e:
            print(e)
