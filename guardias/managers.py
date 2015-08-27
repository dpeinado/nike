 #-*- coding: utf-8 -*-

from django.db import models
from datetime import datetime, date, timedelta
from django.core.exceptions import ObjectDoesNotExist

from guardias.exceptions import NoExisteCalendario, ConsistenciaCalendario

class guardiasManager(models.Manager):

    def check_existencia(self, year):
        try:
            primerdia = datetime(year, 1, 1).toordinal()
            guardia1 = self.get(pk=primerdia)
        except ObjectDoesNotExist:
            raise NoExisteCalendario("No existe el calendario para el año {}".format(year))


    def check_consistencia(self, year):
        self.check_existencia(year)
        inicio = datetime(year, 1, 1).toordinal()
        finaño = datetime(year, 12, 31).toordinal()
        misdias = super(guardiasManager, self).get_queryset().filter(id__gte=inicio, id__lte=finaño)
        if (finaño-inicio+1) != len(misdias):
            raise ConsistenciaCalendario(
                "Error: intervalo entre final y principio de año no coincide con días devueltos")
        for guardia in misdias:
            self.check_fecha(guardia)
        return misdias

    def check_fecha(self, dia):
        if dia.fecha.toordinal() != dia.id:
            raise ConsistenciaCalendario(
                "Error: guardia con fecha no coincidente con el ordinal"
            )

    def set_allSundays(self, year):
        for d in alldaysinyear(year, 6):
            g = self.get(pk=d.toordinal())
            g.tipo = self.model.FES_LAB
            g.save()

    def set_allSaturdays(self, year):
        for d in alldaysinyear(year, 5):
            g = self.get(pk=d.toordinal())
            g.tipo = self.model.FES_FES
            g.save()


def alldaysinyear(year, day):
   d = date(year, 1, 1)                    # January 1st
   d += timedelta(days = day - d.weekday())  # First Sunday
   while d.year == year:
      yield d
      d += timedelta(days = 7)