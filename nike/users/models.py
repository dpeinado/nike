# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from datetime import date, datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from guardias.exceptions import IllegalArgumentError
from .managers import MyUserManager

@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    centro = models.ForeignKey('guardias.Centro', blank=True, null=True)

    guardias = MyUserManager()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def num_guardias_tipo_asignadas(self, hoy, tipo):
        from guardias.models import Guardia
        if not isinstance(hoy, date):
            raise IllegalArgumentError("Error en los argumentos a num_guardias_tipo_asignadas")
        añocorriente = hoy.year
        inicio = date(añocorriente, 1, 1)
        return Guardia.objects.filter(
            owner = self
        ).filter(
            fecha__gte=inicio
        ).filter(
            fecha__lte=hoy
        ).filter(
            tipo=tipo
        ).count()

    def num_guardias_total_asignadas(self, hoy, tipo):
        from guardias.models import Guardia
        if not isinstance(hoy, date):
            raise IllegalArgumentError("Error en los argumentos a num_guardias_total_asignadas")
        añocorriente = hoy.year
        inicio = date(añocorriente, 1, 1)
        return Guardia.objects.filter(
            owner = self
        ).filter(
            fecha__gte=inicio
        ).filter(
            fecha__lte=hoy
        ).count()

    def num_last_year_total_shifts(self, hoy):
        añocorriente = hoy.year
        inicio = date(añocorriente-1, 1, 1)
        fin = date(añocorriente-1, 12, 31)
        from guardias.models import Guardia

        queryset = Guardia.objects.filter(
            owner=self
        ).filter(
            fecha__gte=inicio
        ).filter(
            fecha__lte=fin
        ).count()
        return queryset