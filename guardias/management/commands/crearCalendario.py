from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from guardias.models import Guardia


class Command(BaseCommand):
    help = 'Crea un calendario Nuevo. Arg. Año de creación'

    def add_arguments(self, parser):
        parser.add_argument('year', nargs='+', type=int)

    def handle(self, *args, **options):
        my_year = options['year'][0]
        if self.check_existence(my_year):
            self.stdout.write('Error: este año ({}) ya se encuentra en la base de datos'.format(my_year))
            return
        else:
            self.crear_calendario(my_year)
            self.stdout.write('OK: Calendario creado para el año {}'.format(my_year))

    def check_existence(self, myYear):
        try:
            primerdia = datetime(myYear, 1, 1).toordinal()
            guardia1 = Guardia.objects.get(pk=primerdia)
            return True
        except Guardia.DoesNotExist:
            return False

    def crear_calendario(self, myYear):
        inicio = datetime(myYear, 1, 1).toordinal()
        finaño = datetime(myYear, 12, 31).toordinal()
        for anio in range(inicio, finaño):
            Guardia.objects.create(
                fecha = datetime.fromordinal(anio)
            )