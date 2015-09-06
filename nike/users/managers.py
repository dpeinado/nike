 #-*- coding: utf-8 -*-

from django.db import models
from datetime import datetime, date, timedelta
from operator import itemgetter
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import UserManager

from guardias.exceptions import IllegalArgumentError


class MyUserManager(UserManager):

    def get_next_user_tipo(self, tipo, hoy, micentro):
        from guardias.models import Guardia
        usuarios = self.filter(centro=micentro)
        respuesta = []
        for usuario in usuarios:
            cuantas = usuario.num_guardias_tipo_asignadas(hoy, tipo)
            totales = usuario.num_guardias_total_asignadas(hoy, tipo)
            lastyear = usuario.num_last_year_total_shifts(hoy)
            respuesta.append([cuantas, totales, lastyear, usuario.name, usuario])
        return sorted(respuesta, key=itemgetter(0, 1, 2, 3))






