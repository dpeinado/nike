from datetime import datetime, date
from django.core.management.base import BaseCommand, CommandError
from guardias.models import Guardia
from guardias.exceptions import NoExisteCalendario, ConsistenciaCalendario, ExisteCalendario

class Command(BaseCommand):
    help = """
            Quinto de los comandos para inicializar que se tiene que correr
           """


    def add_arguments(self, parser):
        parser.add_argument('year', nargs='+', type=int)
        parser.add_argument('centro_id', nargs='+', type=int)

    def handle(self, *args, **options):
        year = options['year'][0]
        centro_id = options['centro_id'][0]

        Guardia.objects.program_shifts_all_year(year, centro_id)
        inicio = date(2015,2,1)
        fin = date(2015,2,28)
        # Guardia.objects.
        Guardia.objects.get_dias_tipo_intervalo(inicio, fin, 0,1)
