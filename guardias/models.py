from datetime import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from nike.users.models import User
from guardias.managers import guardiasManager
# Create your models here.


@python_2_unicode_compatible
class Organizacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Centro(models.Model):
    nombre = models.CharField(max_length=100)
    organizacion = models.ForeignKey(Organizacion, blank=True, null=True)
    supervisor = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Guardia(models.Model):
    LAB_LAB = 0
    LAB_LAB_FES = 1
    LAB_FES = 2
    FES_FES = 3
    FES_LAB = 4
    TIPOS_GUARDIA = [(LAB_LAB, """
                        Día laborable con día posterior laborable,
                        pero que la libranza no se enlaza con un festivo.
                        (Tipo lunes, martes o miércoles en semana sin festivos)"""),
                     (LAB_LAB_FES, """
                        Día laborable con día posterior laborable,
                        pero que la libranza si que se enlaza con festivo.
                        (Tipo jueves en semama sin festivos)"""),
                     (LAB_FES, """
                        Día laborable con día posterior festivo.
                        (Tipo viernes en semanas sin festivos)"""),
                     (FES_FES, """
                        Día festivo con día posterior festivo.
                        (Tipo sábado en semanas sin festivos)"""),
                     (FES_LAB, """
                        Día festivo con día posterior laborable.
                        (Tipo Domingo en semanas sin festivos)""")]
    id = models.IntegerField(primary_key=True, unique=True)
    fecha = models.DateField()
    tipo = models.IntegerField(choices=TIPOS_GUARDIA, default=LAB_LAB, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, related_name="owner")
    doneby = models.ForeignKey(User, null=True, related_name="doneby")
    ausencias = models.ManyToManyField(User, related_name='vacaciones')

    objects = guardiasManager()

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.id = self.fecha.toordinal()
        super(Guardia, self).save()

    def __str__(self):
        return "{0}: {1} -- {2}".format(self.fecha, self.tipo, self.owner)




@python_2_unicode_compatible
class VacacionesAnuales(models.Model):
    persona = models.ForeignKey(User)
    año = models.IntegerField()
    dias_de_vacaciones = models.IntegerField(default=22)

    @property
    def dias_disfrutados(self, comienzo, final):
        pass

    @property
    def dias_restantes(self, comienzo, final):
        pass


# @python_2_unicode_compatible
# class PeriodoVacaciones(models.Model):
#     vacaciones = models.ForeignKey(VacacionesAnuales, related_name='periodos')
#     comienzo = models.DateField()
#     final = models.DateField()
#
#     @property
#     def dias(self):
#         return (self.final-self.comienzo).days-Guardia.objects.get_num_festivos(self.comienzo, self.final)+1