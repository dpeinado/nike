from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from guardias.models import Guardia

class Command(BaseCommand):
    help = 'Crea un calendario Nuevo. Arg. Año de creación'

    def add_arguments(self, parser):
        parser.add_argument('year', nargs='+', type=int)

    def handle(self, *args, **options):
        my_year = options['year']
        try:
            str1 = '{} 01 01'.format(my_year)
            primerdia = datetime.strptime(
                str1,
                '%Y %m %d'
            ).toordinal()
            guardia1 = Guardia.objects.get(pk=primerdia)
        except Guardia.DoesNotExist:
            crear_calendario(my_year)

        self.stdout.write('Este año ({}) ya se encuentra en la base de datos'.format(my_year))

    def crear_calendario(self, myYear):
        Guardia.objects.create(
            fecha = datetime.strptime(
                '{} 01 01'.format(my_year),
                '%Y %m %d')
        )