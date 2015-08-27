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
    LAB_LIB_FES = 1
    LAB_FES = 2
    FES_FES = 3
    FES_LAB = 4
    TIPOS_GUARDIA = [(LAB_LAB, """
                        Día laborable con día posterior laborable,
                        pero que la libranza no se enlaza con un festivo.
                        (Tipo lunes, martes o miércoles en semana sin festivos)"""),
                     (LAB_LIB_FES, """
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

    objects = guardiasManager()

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.id = datetime.toordinal(self.fecha)
        super(Guardia, self).save()

    def __str__(self):
        return "{0}: {1} -- {2}".format(self.fecha, self.tipo, self.owner)