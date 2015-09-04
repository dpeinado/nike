 #-*- coding: utf-8 -*-

# python imports
from datetime import datetime, date
# django imports
from test_plus.test import TestCase
from django.core.management import call_command
# third parties imports
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key
# app imports
from guardias.models import Guardia, VacacionesAnuales
from nike.users.models import User


class TestSimples(TestCase):

    def test_setallsundays(self):
        Guardia.objects.crea_calendario(2015)
        Guardia.objects.check_consistencia(2015)
        Guardia.objects.set_allSundaysSaturdays(2015)
        uno    = Guardia.objects.get(fecha=date(2015, 1, 4))
        dos    = Guardia.objects.get(fecha=date(2015, 3, 8))
        tres   = Guardia.objects.get(fecha=date(2015, 9, 13))
        cuatro = Guardia.objects.get(fecha=date(2015, 9, 15))
        self.assertEqual(uno.tipo, Guardia.FES_FES)
        self.assertEqual(dos.tipo, Guardia.FES_FES)
        self.assertEqual(tres.tipo, Guardia.FES_FES)
        self.assertEqual(cuatro.tipo, Guardia.LAB_LAB)

    def test_setallsaturdays(self):
        Guardia.objects.crea_calendario(2015)
        Guardia.objects.check_consistencia(2015)
        Guardia.objects.set_allSaturdays(2015)
        uno    = Guardia.objects.get(fecha=date(2015, 1, 3))
        dos    = Guardia.objects.get(fecha=date(2015, 3, 7))
        tres   = Guardia.objects.get(fecha=date(2015, 9, 12))
        cuatro = Guardia.objects.get(fecha=date(2015, 9, 15))
        self.assertEqual(uno.tipo, Guardia.FES_FES)
        self.assertEqual(dos.tipo, Guardia.FES_FES)
        self.assertEqual(tres.tipo, Guardia.FES_FES)
        self.assertEqual(cuatro.tipo, Guardia.LAB_LAB)

    def test_get_numDiasTipos(self):
        Total = 0
        Guardia.objects.set_calendario(2015, 'festivos.txt')
        mtipo = Guardia.LAB_LAB
        respuesta = Guardia.objects.get_dias_tipo_year(2015, mtipo)
        # print("Tipo {}: {}".format(mtipo, len(respuesta)))
        self.assertEqual(len(respuesta), 140)
        Total += len(respuesta)
        mtipo = Guardia.LAB_LAB_FES
        respuesta = Guardia.objects.get_dias_tipo_year(2015, mtipo)
        # print("Tipo {}: {}".format(mtipo, len(respuesta)))
        self.assertEqual(len(respuesta), 51)
        Total += len(respuesta)
        mtipo = Guardia.LAB_FES
        respuesta = Guardia.objects.get_dias_tipo_year(2015, mtipo)
        # print("Tipo {}: {}".format(mtipo, len(respuesta)))
        self.assertEqual(len(respuesta), 58)
        Total += len(respuesta)
        mtipo = Guardia.FES_FES
        respuesta = Guardia.objects.get_dias_tipo_year(2015, mtipo)
        # print("Tipo {}: {}".format(mtipo, len(respuesta)))
        self.assertEqual(len(respuesta), 53)
        Total += len(respuesta)
        mtipo = Guardia.FES_LAB
        respuesta = Guardia.objects.get_dias_tipo_year(2015, mtipo)
        # print("Tipo {}: {}".format(mtipo, len(respuesta)))
        self.assertEqual(len(respuesta), 63)
        Total += len(respuesta)
        # print("---------------------------------------------")
        # print("Total = {}".format(Total))
        self.assertEqual(Total, 365)

    def test_get_calendario(self):
        Guardia.objects.set_calendario(2015, 'festivos.txt')
        uno = Guardia.objects.get_calendario(2015)
        self.assertEqual(uno[0][0], 51)
        self.assertEqual(uno[1][0], 53)
        self.assertEqual(uno[2][0], 58)
        self.assertEqual(uno[3][0], 63)
        self.assertEqual(uno[4][0], 140)

    def test_get_num_festivos(self):
        Guardia.objects.set_calendario(2015, 'festivos.txt')
        respuesta=Guardia.objects.get_num_festivos(date(2015,1,1), date(2015,2,15))
        self.assertEqual(respuesta,17)

    def test_set_vacaciones(self):
        from core.utility import get_range_dates_list
        Guardia.objects.set_calendario(2015, 'festivos.txt')
        user1 = self.make_user()
        l1 = get_range_dates_list(date(2015,1,28), date(2015,2,7))
        l2 =[date(2015,5,8),date(2015,6,20)]
        lista_vacaciones = l1+l2
        Guardia.objects.set_vacaciones(lista_vacaciones, user1)
        for dia in lista_vacaciones:
            mio=Guardia.objects.get(pk=dia.toordinal())
            self.assertEqual(mio.ausencias.all()[0], user1)


class TestComplejos(TestCase):
    def setUp(self):
        nombres = ['uno', 'dos', 'tres', 'cuatro', 'cinco',
                   'seis', 'siete', 'ocho', 'nueve', 'diez',
                   'once', 'doce', 'trece', 'catorce']



        for nombre in nombres:
            mommy.make('User', name=nombre)
            usuario = User.objects.get(name=nombre)
            VacacionesAnuales.objects.create(
                persona=usuario,
                año=2015,
                dias_de_vacaciones=22
            )
        mommy.make('organizacion.centro', supervisor=usuario)
        pass

