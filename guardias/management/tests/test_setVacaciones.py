from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from model_mommy import mommy

class setVacacionesTest(TestCase):
    def setUp(self):
        nombres = ['uno', 'dos', 'tres', 'cuatro', 'cinco',
                   'seis', 'siete', 'ocho', 'nueve', 'diez',
                   'once', 'doce', 'trece', 'catorce']

        self.organ = mommy.make('guardias.organizacion', nombre='Infanta Sofía, Servicio RX')
        self.centro = mommy.make('guardias.centro', organizacion=self.organ)

        usuarios=[]
        for nombre in nombres:
            usuario = mommy.make('users.User', name=nombre, centro=self.centro)
            usuarios.append(usuario)

        self.centro.supervisor=usuario
        self.centro.save()

    def test_crearVacaciones(self):
        out = StringIO()
        call_command('setVacaciones', '2015', '22', str(self.centro.pk), stdout=out)
        print(out.getvalue())
        self.assertIn('Ok', out.getvalue())
        call_command('setVacaciones', '2015', '22', str(self.centro.pk), stdout=out)
        print(out.getvalue())
        self.assertIn('Error', out.getvalue())