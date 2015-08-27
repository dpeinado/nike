from datetime import datetime
from test_plus.test import TestCase
from guardias.models import Organizacion, Centro, Guardia


class TestCentro(TestCase):
    def setUp(self):

        self.organizacion = Organizacion.objects.create(
            nombre='Hospital Infanta Sofía')

        self.centro1 = Centro.objects.create(
            nombre = 'Servicio de Radiodiagnóstico')

        self.user = self.make_user()

    def test_crearorganizacion(self):
        # Comprobar creación de organización
        self.assertEqual(
            self.organizacion.__str__(),
            'Hospital Infanta Sofía')

    def test_centro1(self):
        # comprobar creación de centro sin organicación ni supervisor
        self.assertEqual(
            self.centro1.__str__(),
            'Servicio de Radiodiagnóstico')
        self.assertEqual(self.centro1.organizacion, None)
        self.assertEqual(self.centro1.supervisor,None)

    def test_centro2(self):
        # comprobar creación de centro con organización y supervisor
        self.centro2 = Centro.objects.create(
            nombre = 'Servicio de Radiodiagnóstico',
            organizacion = self.organizacion,
            supervisor = self.user)
        self.assertEqual(self.centro2.organizacion, self.organizacion)
        self.assertEqual(self.centro2.supervisor, self.user)

class TestGuardia(TestCase):

    def test_creacion(self):
        self.guardia = Guardia.objects.create(
            fecha = datetime(2015, 8, 26).date(),
            tipo = Guardia.LAB_LAB
        )
        self.assertEqual(self.guardia.id,
                         735836)
        self.assertEqual(self.guardia.tipo,
                         0)

