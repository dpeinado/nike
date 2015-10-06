 #-*- coding: utf-8 -*-

# python imports
from datetime import datetime, date
import csv
import random

# django imports
from test_plus.test import TestCase
from django.core.management import call_command
# third parties imports
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key
# app imports
from guardias.models import Guardia, VacacionesAnuales, Centro, Organizacion
from nike.users.models import User


class TestSimples(TestCase):
    def setUp(self):
        nombres = ['uno', 'dos', 'tres', 'cuatro', 'cinco',
                   'seis', 'siete', 'ocho', 'nueve', 'diez',
                   'once', 'doce', 'trece', 'catorce']

        self.organ = mommy.make('guardias.organizacion', nombre='Infanta Sofía, Servicio RX')
        self.centro = mommy.make('guardias.centro', organizacion=self.organ)
        self.centro2 =mommy.make('guardias.centro', organizacion=self.organ)


    def test_setallsundays(self):
        Guardia.objects.crea_calendario(2015, self.centro.id)
        Guardia.objects.check_consistencia(2015, self.centro.id)
        Guardia.objects.set_allSundaysSaturdays(2015, self.centro.id)
        uno    = Guardia.objects.get(fecha=date(2015, 1, 4).toordinal(), centro=self.centro.id)
        dos    = Guardia.objects.get(fecha=date(2015, 3, 8).toordinal(), centro=self.centro.id)
        tres   = Guardia.objects.get(fecha=date(2015, 9, 13).toordinal(), centro=self.centro.id)
        cuatro = Guardia.objects.get(fecha=date(2015, 9, 15).toordinal(), centro=self.centro.id)
        self.assertEqual(uno.tipo, Guardia.FES_FES)
        self.assertEqual(dos.tipo, Guardia.FES_FES)
        self.assertEqual(tres.tipo, Guardia.FES_FES)
        self.assertEqual(cuatro.tipo, Guardia.LAB_LAB)

    def test_setallsaturdays(self):
        Guardia.objects.crea_calendario(2015, self.centro.id)
        Guardia.objects.check_consistencia(2015, self.centro.id)
        Guardia.objects.set_allSaturdays(2015, self.centro.id)
        uno    = Guardia.objects.get(fecha=date(2015, 1, 3).toordinal(), centro=self.centro.id)
        dos    = Guardia.objects.get(fecha=date(2015, 3, 7).toordinal(), centro=self.centro.id)
        tres   = Guardia.objects.get(fecha=date(2015, 9, 12).toordinal(), centro=self.centro.id)
        cuatro = Guardia.objects.get(fecha=date(2015, 9, 15).toordinal(), centro=self.centro.id)
        self.assertEqual(uno.tipo, Guardia.FES_FES)
        self.assertEqual(dos.tipo, Guardia.FES_FES)
        self.assertEqual(tres.tipo, Guardia.FES_FES)
        self.assertEqual(cuatro.tipo, Guardia.LAB_LAB)

    def test_set_calendario(self):
        Guardia.objects.set_calendario(2015, 'ficheros/festivos.txt', self.centro.id)
        festivos = list(
            Guardia.objects.filter(tipo=Guardia.FES_FES)
        )+list(
            Guardia.objects.filter(tipo=Guardia.FES_LAB)
        )
        with open('ficheros/festivos.txt', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                unfestivo = Guardia.objects.get(fecha=datetime.strptime(row[0], "%Y-%m-%d").date().toordinal())
                self.assertIn(unfestivo, festivos)


    def test_get_numDiasTipos(self):
        Total = 0
        Guardia.objects.set_calendario(2015, 'ficheros/festivos.txt', self.centro.id)
        mtipo = Guardia.LAB_LAB
        respuesta = Guardia.objects.get_dias_tipo_year(2015, mtipo, self.centro.id)
        # print("Tipo {}: {}".format(mtipo, len(respuesta)))
        self.assertEqual(len(respuesta), 140)
        Total += len(respuesta)
        mtipo = Guardia.LAB_LAB_FES
        respuesta = Guardia.objects.get_dias_tipo_year(2015, mtipo, self.centro.id)
        # print("Tipo {}: {}".format(mtipo, len(respuesta)))
        self.assertEqual(len(respuesta), 51)
        Total += len(respuesta)
        mtipo = Guardia.LAB_FES
        respuesta = Guardia.objects.get_dias_tipo_year(2015, mtipo, self.centro.id)
        # print("Tipo {}: {}".format(mtipo, len(respuesta)))
        self.assertEqual(len(respuesta), 58)
        Total += len(respuesta)
        mtipo = Guardia.FES_FES
        respuesta = Guardia.objects.get_dias_tipo_year(2015, mtipo, self.centro.id)
        # print("Tipo {}: {}".format(mtipo, len(respuesta)))
        self.assertEqual(len(respuesta), 53)
        Total += len(respuesta)
        mtipo = Guardia.FES_LAB
        respuesta = Guardia.objects.get_dias_tipo_year(2015, mtipo, self.centro.id)
        # print("Tipo {}: {}".format(mtipo, len(respuesta)))
        self.assertEqual(len(respuesta), 63)
        Total += len(respuesta)
        # print("---------------------------------------------")
        # print("Total = {}".format(Total))
        self.assertEqual(Total, 365)

    def test_get_calendario(self):
        Guardia.objects.set_calendario(2015, 'ficheros/festivos.txt', self.centro.id)
        uno = Guardia.objects.get_calendario(2015, self.centro.id)
        self.assertEqual(uno[0][0], 51)
        self.assertEqual(uno[1][0], 53)
        self.assertEqual(uno[2][0], 58)
        self.assertEqual(uno[3][0], 63)
        self.assertEqual(uno[4][0], 140)

    def test_get_num_festivos(self):
        Guardia.objects.set_calendario(2015, 'ficheros/festivos.txt', self.centro.id)
        respuesta=Guardia.objects.get_num_festivos(date(2015,1,1), date(2015,2,15), self.centro.id)
        self.assertEqual(respuesta,17)

    def test_set_vacaciones(self):
        from core.utility import get_range_dates_list
        Guardia.objects.set_calendario(2015, 'ficheros/festivos.txt', self.centro.id)
        user1 = self.make_user()
        l1 = get_range_dates_list(date(2015,1,28), date(2015,2,7))
        l2 =[date(2015,5,8),date(2015,6,20)]
        lista_vacaciones = l1+l2
        Guardia.objects.set_vacaciones(lista_vacaciones, user1)
        for dia in lista_vacaciones:
            mio=Guardia.objects.get(fecha=dia.toordinal())
            self.assertEqual(mio.ausencias.all()[0], user1)


class TestComplejos(TestCase):
    def setUp(self):
        nombres = ['uno', 'dos', 'tres', 'cuatro', 'cinco',
                   'seis', 'siete', 'ocho', 'nueve', 'diez',
                   'once', 'doce', 'trece', 'catorce']

        nombres2 = ['uno2', 'dos2', 'tres2', 'cuatro2', 'cinco2']

        self.organ = mommy.make('guardias.organizacion', nombre='Infanta Sofía, Servicio RX')
        self.centro = mommy.make('guardias.centro', organizacion=self.organ, nombre="Centro1")
        self.centro2= mommy.make('guardias.centro', organizacion=self.organ, nombre="Centro2")

        usuarios=[]
        for nombre in nombres:
            usuario = mommy.make('users.User', name=nombre, centro=self.centro)
            usuarios.append(usuario)
            VacacionesAnuales.objects.create(
                persona=usuario,
                año=2015,
                dias_de_vacaciones=22
            )
        self.centro.supervisor=usuario
        self.centro.save()

        usuarios=[]
        for nombre in nombres2:
            usuario = mommy.make('users.User', name=nombre, centro=self.centro2)
            usuarios.append(usuario)
            VacacionesAnuales.objects.create(
                persona=usuario,
                año=2015,
                dias_de_vacaciones=25
            )
        self.centro2.supervisor=usuario
        self.centro2.save()


        Guardia.objects.set_calendario(2015, 'ficheros/festivos.txt', self.centro.id)
        Guardia.objects.set_calendario(2014, 'ficheros/festivos_old.txt', self.centro.id)
        Guardia.objects.set_calendario(2015, 'ficheros/festivos2.txt', self.centro2.id)
        Guardia.objects.set_calendario(2014, 'ficheros/festivos_old2.txt', self.centro2.id)

    def test_grande1(self):
        print('Test Grande 1')

        usuarios1 = User.objects.filter(centro=self.centro.id)
        self.assertEqual(len(usuarios1), 14)
        vacaciones = VacacionesAnuales.objects.filter(persona__centro_id=self.centro.id)
        self.assertEqual(len(vacaciones), 14)
        cent1 = Centro.objects.get(pk = self.centro.id)
        self.assertEqual(cent1.supervisor.name, 'catorce')
        self.assertEqual(cent1.nombre, 'Centro1')
        self.assertEqual(cent1.organizacion.nombre, 'Infanta Sofía, Servicio RX')

        usuarios2 = User.objects.filter(centro=self.centro2.id)
        self.assertEqual(len(usuarios2), 5)
        vacaciones = VacacionesAnuales.objects.filter(persona__centro_id=self.centro2.id)
        self.assertEqual(len(vacaciones), 5)
        cent2 = Centro.objects.get(pk = self.centro2.id)
        self.assertEqual(cent2.supervisor.name, 'cinco2')
        self.assertEqual(cent2.nombre, 'Centro2')


        corriente1 = Guardia.objects.get_all_shifts_year(2015, self.centro.id)
        anterior1  = Guardia.objects.get_all_shifts_year(2014, self.centro.id)
        self.assertEqual(len(corriente1), 365)
        self.assertEqual(len(anterior1), 365)
        corriente2 = Guardia.objects.get_all_shifts_year(2015, self.centro2.id)
        anterior2  = Guardia.objects.get_all_shifts_year(2014, self.centro2.id)
        self.assertEqual(len(corriente2), 365)
        self.assertEqual(len(anterior2), 365)

        random.seed(1)
        for g in (list(corriente1)+list(anterior1)):
            g.owner = random.choice(usuarios1)
            g.save()
        for g in (list(corriente2)+list(anterior2)):
            g.owner = random.choice(usuarios2)
            g.save()


        hoy = date(2015,12,31).toordinal()
        totales = []
        for usuario in usuarios1:
            subtotal = 0
            for tipo, leyenda in Guardia.TIPOS_GUARDIA:
                cuantas = usuario.num_guardias_tipo_asignadas(hoy, tipo)
                subtotal += cuantas
                print('Usuario: {} tiene {} guardias del tipo {}'.format(
                    usuario.name,
                    cuantas,
                    tipo
                ))
            totales.append([usuario.name, subtotal])
        for res1, res2 in totales:
            print(res1, ": ", res2)

        totales = []
        for usuario in usuarios2:
            subtotal = 0
            for tipo, leyenda in Guardia.TIPOS_GUARDIA:
                cuantas = usuario.num_guardias_tipo_asignadas(hoy, tipo)
                subtotal += cuantas
                print('Usuario: {} tiene {} guardias del tipo {}'.format(
                    usuario.name,
                    cuantas,
                    tipo
                ))
            totales.append([usuario.name, subtotal])
        for res1, res2 in totales:
            print(res1, ": ", res2)

    def test_grande2(self):
        print('Test Grande 2')

        hoy = date(2015,6,15).toordinal()

        respuesta = Guardia.objects.program_shifts_all_year(2015, self.centro)
        pass
