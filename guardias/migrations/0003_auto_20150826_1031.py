# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guardias', '0002_guardia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guardia',
            name='tipo',
            field=models.IntegerField(null=True, blank=True, choices=[(0, '\n                        Día laborable con día posterior laborable,\n                        pero que la libranza no se enlaza con un festivo.\n                        (Tipo lunes, martes o miércoles en semana sin festivos)'), (1, '\n                        Día laborable con día posterior laborable,\n                        pero que la libranza si que se enlaza con festivo.\n                        (Tipo jueves en semama sin festivos)'), (2, '\n                        Día laborable con día posterior festivo.\n                        (Tipo viernes en semanas sin festivos)'), (3, '\n                        Día festivo con día posterior festivo.\n                        (Tipo sábado en semanas sin festivos)'), (4, '\n                        Día festivo con día posterior laborable.\n                        (Tipo Domingo en semanas sin festivos)')]),
        ),
    ]
