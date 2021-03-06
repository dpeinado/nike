from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from guardias.models import Guardia
from guardias.exceptions import NoExisteCalendario, ConsistenciaCalendario, ExisteCalendario

class Command(BaseCommand):
    help = """
            Cuarto de los comandos para inicializar que se tiene que correr
           """


    def add_arguments(self, parser):
        parser.add_argument('fichero', nargs='+')
        parser.add_argument('year', nargs='+', type=int)
        parser.add_argument('centro_id', nargs='+', type=int)

    def handle(self, *args, **options):
        filename = options['fichero'][0]
        year = options['year'][0]
        centro_id = options['centro_id'][0]


        # Gestionar las excepciones
        try:
            Guardia.objects.set_calendario(year, filename, centro_id)
            self.stdout.write("OK")
        except:
            self.stdout.write("Error")