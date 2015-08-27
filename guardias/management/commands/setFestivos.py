from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from guardias.models import Guardia
from guardias.exceptions import NoExisteCalendario, ConsistenciaCalendario

class Command(BaseCommand):
    help = """
        Lee de un fichero texto AAAA MM DD, los festivos del año
        y después hace el cálculo para categorizar los días."""

    def add_arguments(self, parser):
        parser.add_argument('year', nargs='+', type=int)

    def handle(self, *args, **options):
        year = options['year'][0]
