 #-*- coding: utf-8 -*-
from test_plus.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO
from guardias.models import Guardia
from datetime import datetime, date

class TestSetSundays(TestCase):

    def test_setallsundays(self):
        out = StringIO()
        call_command('crearCalendario', '2015', stdout=out)
        self.assertIn('OK', out.getvalue())
        Guardia.objects.set_allSundays(2015)
        uno    = Guardia.objects.get(fecha=date(2015, 1, 4))
        dos    = Guardia.objects.get(fecha=date(2015, 3, 8))
        tres   = Guardia.objects.get(fecha=date(2015, 9, 13))
        cuatro = Guardia.objects.get(fecha=date(2015, 9, 15))
        self.assertEqual(uno.tipo, Guardia.FES_LAB)
        self.assertEqual(dos.tipo, Guardia.FES_LAB)
        self.assertEqual(tres.tipo, Guardia.FES_LAB)
        self.assertEqual(cuatro.tipo, Guardia.LAB_LAB)

    def test_setallsaturdays(self):
        out = StringIO()
        call_command('crearCalendario', '2015', stdout=out)
        self.assertIn('OK', out.getvalue())
        Guardia.objects.set_allSaturdays(2015)
        uno    = Guardia.objects.get(fecha=date(2015, 1, 3))
        dos    = Guardia.objects.get(fecha=date(2015, 3, 7))
        tres   = Guardia.objects.get(fecha=date(2015, 9, 12))
        cuatro = Guardia.objects.get(fecha=date(2015, 9, 15))
        self.assertEqual(uno.tipo, Guardia.FES_FES)
        self.assertEqual(dos.tipo, Guardia.FES_FES)
        self.assertEqual(tres.tipo, Guardia.FES_FES)
        self.assertEqual(cuatro.tipo, Guardia.LAB_LAB)