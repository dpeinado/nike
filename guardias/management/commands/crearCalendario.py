from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from guardias.models import Guardia
from guardias.exceptions import NoExisteCalendario, ConsistenciaCalendario

class Command(BaseCommand):
    help = 'Crea un calendario Nuevo. Arg. Año de creación'

    def add_arguments(self, parser):
        parser.add_argument('year', nargs='+', type=int)

    def handle(self, *args, **options):
        year = options['year'][0]
        try:
            Guardia.objects.check_existencia(year)
            self.stdout.write('Error: este año ({}) ya se encuentra en la base de datos'.format(year))
            return
        except NoExisteCalendario:
            inicio = datetime(year, 1, 1).toordinal()
            finaño = datetime(year, 12, 31).toordinal()
            for anio in range(inicio, finaño+1):
                Guardia.objects.create(
                    fecha = datetime.fromordinal(anio)
                )
            self.stdout.write('OK: Calendario creado para el año {}'.format(year))

