from django.core.management.base import BaseCommand
from guardias.models import Organizacion, Centro
from django.core.exceptions import ObjectDoesNotExist
import csv

class Command(BaseCommand):
    help = """
            Primero de los comandos para inicializar que se tiene que correr
           """

    def add_arguments(self, parser):
        parser.add_argument('fichero', nargs='+')

    def handle(self, *args, **options):
        filename = options['fichero'][0]

        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                centro = row[0]
                organizacion = row[1]
                try:
                    org1 = Organizacion.objects.get(nombre=organizacion)
                except ObjectDoesNotExist:
                    org1 = Organizacion.objects.create(nombre=organizacion)
                try:
                    cent1 = Centro.objects.get(nombre=centro)
                except ObjectDoesNotExist:
                    cent1 = Centro.objects.create(nombre=centro, organizacion=org1)