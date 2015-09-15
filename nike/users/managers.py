 #-*- coding: utf-8 -*-

from operator import itemgetter
from django.contrib.auth.models import UserManager

import collections

class MyUserManager(UserManager):

    def get_next_user_tipo(self, tipo, hoy, micentro, nlugares):
        usuariosSinOrden = self.filter(centro=micentro).order_by('username')
        usuarios = collections.deque(list(usuariosSinOrden))
        usuarios.rotate(nlugares)
        respuesta = []
        for usuario in usuarios:
            cuantas = usuario.num_guardias_tipo_asignadas(hoy, tipo)
            totales = usuario.num_guardias_total_hasta_fin_mes_asignadas(hoy)
            lastyear = usuario.num_last_year_total_shifts(hoy)
            respuesta.append([cuantas, totales, lastyear, usuario.username, usuario])
        l1 = sorted(respuesta, key=itemgetter(0, 1, 2))
        # l2 = collections.deque(l1)
        # l2.rotate(nlugares)
        return l1






