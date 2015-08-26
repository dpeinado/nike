from test_plus.test import TestCase
from guardias.models import Organizacion, Centro


class TestCentro(TestCase):
    def setUp(self):
        self.organizacion = Organizacion.objects.create(
            nombre='Hospital Infanta Sofía',
                                                        )

    def crearCentroSinOrganizacion(self):
        self.centro1 = Centro.objects.create(
            nombre = "Servicio de Radiodiagnóstico"
        )
        self.assertEqual(
            self.organizacion.__str__(),
            'Hospital Infanta Sofía'
        )
        self.assertEqual(
            self.centro1.__str__(),
            "Servicio de Radiodiagnóstico"
        )