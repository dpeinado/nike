from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

class createCalendarTest(TestCase):

    def test_creacion_error(self):
        out = StringIO()
        call_command('crearCalendario', 'festivos.txt', '2015', stdout=out)
        print(out.getvalue())
        self.assertIn('OK', out.getvalue())
        call_command('crearCalendario', 'festivos.txt', '2015', stdout=out)
        print(out.getvalue())
        self.assertIn('Error', out.getvalue())