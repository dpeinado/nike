from datetime import date

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from guardias.managers import guardiasManager, listaGuardiasManager
from nike.users.models import User

# Create your models here.


@python_2_unicode_compatible
class Organizacion(models.Model):
    """
    Clase para definir una organización a la cual pueden pertenecer varios centros
    """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Centro(models.Model):
    """
    Clase que define un centro de trabajo. A este centro están adscritos los trabajadores
    a turnos
    """
    nombre = models.CharField(max_length=100)
    organizacion = models.ForeignKey(Organizacion, blank=True, null=True)
    supervisor = models.ForeignKey(User, related_name='supervisor', blank=True, null=True)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Guardia(models.Model):
    """
    Clase para el calendario de guardias. Se generan 365 por año y centro.
    Los miembros son:
        fecha: entero date.toordinal. Día en el que tiene lugar la guardia
        centro: centro al cual pertenece en calendario de guardias.
        tipo: tipo de guardia. Ver más adelante en la definición de TIPOS_GUARDIA
        owner: el propietario de la guardia. Este es al primero qeu se le asignó.
                Si después se cambia la guardia cuando está congelado el calendario
                el owner se mantiene. Si no está congelado entonces si que puede
                cambiar el owner.
        doneby: es el trabajador que realiza la guardia
        ausencias: se apunta a los trabajadores que este día están ausentes, bien por
                    vacaciones, bien por días de libre disposición, enfermedad, baja, etc.
                    Es importante a la hora de hacer la programación. Una enfermedad de última
                    hora que no afecta al calendario de guardias no hace falta que se introduzca

    """
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
    fecha = models.IntegerField()
    centro = models.ForeignKey(Centro)
    tipo = models.IntegerField(choices=TIPOS_GUARDIA, default=LAB_LAB, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, related_name="owner")
    doneby = models.ForeignKey(User, null=True, related_name="doneby")
    ausencias = models.ManyToManyField(User, related_name='vacaciones')
    fijada = models.BooleanField(default=False)
    pivote = models.BooleanField(default=False)

    objects = guardiasManager()

    class Meta:
        ordering = ['id']

    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         self.id = self.fecha.toordinal()
    #     super(Guardia, self).save()

    def __str__(self):
        return "{0}: {1} -- {2}".format(date.fromordinal(self.fecha), self.tipo, self.owner)


@python_2_unicode_compatible
class ListaGuardias(models.Model):
    """
    Esta clase representa una lista ordenada de personas de un centro y para un tipo de guardia determinada.
    La primera persona es a la que le toca la próxima guardia de este tipo para este centro.
    Solo tiene sentido hacer esto para un centro y un tipo de guardia determinado.
    """

    centro = models.ForeignKey(Centro)
    tipo = models.IntegerField(choices=Guardia.TIPOS_GUARDIA, default=Guardia.LAB_LAB)
    user = models.ForeignKey(User)
    orden = models.IntegerField(default=0)

    objects = listaGuardiasManager()

    class Meta:
        unique_together = (('centro', 'tipo', 'orden'),)

    def __str__(self):
        return "{0}-{1} {2}: {3}".format(self.centro,
                                         self.tipo,
                                         self.user.username,
                                         self.orden)

@python_2_unicode_compatible
class VacacionesAnuales(models.Model):
    """
    Clase para definir el número de días de vacaciones y de libre disposición que se tienen al año
    """
    persona = models.ForeignKey(User)
    año = models.IntegerField()
    dias_de_vacaciones = models.IntegerField(default=22)

    @property
    def dias_disfrutados(self, comienzo, final):
        pass

    @property
    def dias_restantes(self, comienzo, final):
        pass