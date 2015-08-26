# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('guardias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='guardia',
            fields=[
                ('id', models.IntegerField(serialize=False, unique=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('tipo', models.IntegerField(default=0, choices=[(0, '\n                        Día laborable con día posterior laborable,\n                        pero que la libranza no se enlaza con un festivo.\n                        (Tipo lunes, martes o miércoles en semana sin festivos)'), (1, '\n                        Día laborable con día posterior laborable,\n                        pero que la libranza si que se enlaza con festivo.\n                        (Tipo jueves en semama sin festivos)'), (2, '\n                        Día laborable con día posterior festivo.\n                        (Tipo viernes en semanas sin festivos)'), (3, '\n                        Día festivo con día posterior festivo.\n                        (Tipo sábado en semanas sin festivos)'), (4, '\n                        Día festivo con día posterior laborable.\n                        (Tipo Domingo en semanas sin festivos)')])),
                ('doneby', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='doneby')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='owner')),
            ],
        ),
    ]
