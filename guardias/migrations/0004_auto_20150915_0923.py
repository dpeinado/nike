# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('guardias', '0003_auto_20150909_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaGuardias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('tipo', models.IntegerField(choices=[(0, '\n                        Día laborable con día posterior laborable,\n                        pero que la libranza no se enlaza con un festivo.\n                        (Tipo lunes, martes o miércoles en semana sin festivos)'), (1, '\n                        Día laborable con día posterior laborable,\n                        pero que la libranza si que se enlaza con festivo.\n                        (Tipo jueves en semama sin festivos)'), (2, '\n                        Día laborable con día posterior festivo.\n                        (Tipo viernes en semanas sin festivos)'), (3, '\n                        Día festivo con día posterior festivo.\n                        (Tipo sábado en semanas sin festivos)'), (4, '\n                        Día festivo con día posterior laborable.\n                        (Tipo Domingo en semanas sin festivos)')], default=0)),
                ('orden', models.IntegerField(default=0)),
                ('centro', models.ForeignKey(to='guardias.Centro')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='listaguardias',
            unique_together=set([('centro', 'tipo', 'orden')]),
        ),
    ]
