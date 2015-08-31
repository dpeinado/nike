 #-*- coding: utf-8 -*-
from test_plus.test import TestCase
from django.core.management import call_command
from guardias.models import Guardia
from datetime import datetime, date

class TestSetSundays(TestCase):

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
        respuesta = Guardia.objects.get_dias_tipo(2015, mtipo)
        print("Tipo {}: {}".format(mtipo, len(respuesta)))
        Total += len(respuesta)
        mtipo = Guardia.LAB_LAB_FES
        respuesta = Guardia.objects.get_dias_tipo(2015, mtipo)
        print("Tipo {}: {}".format(mtipo, len(respuesta)))
        Total += len(respuesta)
        mtipo = Guardia.LAB_FES
        respuesta = Guardia.objects.get_dias_tipo(2015, mtipo)
        print("Tipo {}: {}".format(mtipo, len(respuesta)))
        Total += len(respuesta)
        mtipo = Guardia.FES_FES
        respuesta = Guardia.objects.get_dias_tipo(2015, mtipo)
        print("Tipo {}: {}".format(mtipo, len(respuesta)))
        Total += len(respuesta)
        mtipo = Guardia.FES_LAB
        respuesta = Guardia.objects.get_dias_tipo(2015, mtipo)
        print("Tipo {}: {}".format(mtipo, len(respuesta)))
        Total += len(respuesta)
        print("---------------------------------------------")
        print("Total = {}".format(Total))