from django.core.management.base import BaseCommand
from guardias.models import Organizacion, Centro
from nike.users.models import User
from django.core.exceptions import ObjectDoesNotExist
import csv

class Command(BaseCommand):
    help = """
            Segundo de los comandos para inicializar que se tiene que correr
           """

    def add_arguments(self, parser):
        parser.add_argument('fichero', nargs='+')

    def handle(self, *args, **options):
        filename = options['fichero'][0]

        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                nombre = row[0]
                apellidos = row[1]
                username = row[2]
                centro_id= row[3]
                try:
                    cent1 = Centro.objects.get(id=centro_id)
                except ObjectDoesNotExist:
                    print("Error: no existe el centro con id: {}".format(centro_id))
                    return

                User.objects.create(
                    first_name=nombre,
                    last_name=apellidos,
                    username=username,
                    centro=cent1
                )