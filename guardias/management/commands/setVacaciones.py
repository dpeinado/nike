from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from guardias.models import Guardia, VacacionesAnuales
from guardias.exceptions import NoExisteCalendario, ConsistenciaCalendario, ExisteCalendario
from nike.users.models import User
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = """
        Lee de la línea de parámetros el año y el número de días
        de vacaciones para todos"""

    def add_arguments(self, parser):
        parser.add_argument('year', nargs='+', type=int)
        parser.add_argument('ndias', nargs='+', type=int)
        parser.add_argument('centro_id', nargs='+', type=int)

    def handle(self, *args, **options):
        year = options['year'][0]
        ndias = options['ndias'][0]
        centro_id = options['centro_id'][0]
        from guardias.models import Centro
        try:
            micentro = Centro.objects.get(pk=centro_id)
        except ObjectDoesNotExist:
            self.stdout.write("Error: no existe centro con id = {}".format(centro_id))
            return
        try:
            usuarios = User.objects.filter(centro=micentro)
        except ObjectDoesNotExist:
            self.stdout.write("Error: no existen usuarios en el centro: {}".format(micentro.nombre))
        for user in usuarios:
            v1=VacacionesAnuales.objects.filter(
                persona=user,
                año=year
            )
            if v1:
                self.stdout.write("Error: Este usuario {}, ya tiene asignados {} días de vacaciones".format(
                    user,ndias)
                )
            else:
                VacacionesAnuales.objects.create(
                    persona=user,
                    año=year,
                    dias_de_vacaciones=ndias
                )
                self.stdout.write("Ok: Calendario de vacaciones creado")