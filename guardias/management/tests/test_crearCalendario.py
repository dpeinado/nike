from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from model_mommy import mommy

class createCalendarTest(TestCase):
    def setUp(self):
        self.organ = mommy.make('guardias.organizacion', nombre='Infanta Sofía, Servicio RX')
        self.centro = mommy.make('guardias.centro', organizacion=self.organ)

    def test_creacion_error(self):
        out = StringIO()
        call_command('crearCalendario', 'festivos.txt', '2015', str(self.centro.pk), stdout=out)
        print(out.getvalue())
        self.assertIn('OK', out.getvalue())
        call_command('crearCalendario', 'festivos.txt', '2015', str(self.centro.pk), stdout=out)
        print(out.getvalue())
        self.assertIn('Error', out.getvalue())