from django.core.management.base import BaseCommand, CommandError
from guardias.models import Guardia
import csv

class Command(BaseCommand):
    help = """
            Sexto. Comprobación de cómo se han puesto las guardias
           """


    def add_arguments(self, parser):
        parser.add_argument('year', nargs='+', type=int)
        parser.add_argument('centro_id', nargs='+', type=int)

    def handle(self, *args, **options):
        year = options['year'][0]
        centro_id = options['centro_id'][0]
        respuesta = Guardia.objects.cuantas_guardias_mes(year, centro_id)

        meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']

        lista = []
        lista.append([" ",]+meses)

        for usuario in respuesta.keys():
            fila=[]
            fila.append(usuario)
            pitos=respuesta[usuario]
            for mes in meses:
                cuala = pitos[mes][5]
                fila.append(cuala)
            lista.append(fila)

        with open('guardias.csv', 'w') as f:
            a = csv.writer(f)
            a.writerows(lista)
