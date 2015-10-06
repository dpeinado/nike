from django.core.management.base import BaseCommand
from guardias.models import Organizacion, Centro, Guardia, ListaGuardias
from nike.users.models import User
from django.core.exceptions import ObjectDoesNotExist
import csv

class Command(BaseCommand):
    help = """
            Segundo de los comandos para inicializar que se tiene que correr
           """

    def add_arguments(self, parser):
        parser.add_argument('fichero', nargs='+')
        parser.add_argument('centro', nargs='+', type=int)

    def handle(self, *args, **options):
        filename = options['fichero'][0]
        centro = options['centro'][0]

        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                nombre = row[0]
                apellidos = row[1]
                username = row[2]
                orden = row[3]

                try:
                    cent1 = Centro.objects.get(id=centro)
                except ObjectDoesNotExist:
                    print("Error: no existe el centro con id: {}".format(centro))
                    return

                myuser = User.objects.create(
                    first_name=nombre,
                    last_name=apellidos,
                    username=username,
                    centro=cent1
                )
                for tipo, descripcion in Guardia.TIPOS_GUARDIA:
                    ListaGuardias.objects.create(
                        centro_id=centro,
                        tipo = tipo,
                        user = myuser,
                        orden = orden
                    )
        cuantosUsers = ListaGuardias.objects.filter(centro=centro,tipo=0).count()
        esc = int(cuantosUsers/len(Guardia.TIPOS_GUARDIA))
        index = 0
        for tipo, descripcion in Guardia.TIPOS_GUARDIA:
            ListaGuardias.objects.shift_n(centro,tipo,esc*index)
            index+=1