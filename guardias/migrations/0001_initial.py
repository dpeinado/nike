# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Centro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Guardia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.IntegerField()),
                ('tipo', models.IntegerField(blank=True, null=True, choices=[(0, '\n                        Día laborable con día posterior laborable,\n                        pero que la libranza no se enlaza con un festivo.\n                        (Tipo lunes, martes o miércoles en semana sin festivos)'), (1, '\n                        Día laborable con día posterior laborable,\n                        pero que la libranza si que se enlaza con festivo.\n                        (Tipo jueves en semama sin festivos)'), (2, '\n                        Día laborable con día posterior festivo.\n                        (Tipo viernes en semanas sin festivos)'), (3, '\n                        Día festivo con día posterior festivo.\n                        (Tipo sábado en semanas sin festivos)'), (4, '\n                        Día festivo con día posterior laborable.\n                        (Tipo Domingo en semanas sin festivos)')], default=0)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Organizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VacacionesAnuales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('año', models.IntegerField()),
                ('dias_de_vacaciones', models.IntegerField(default=22)),
            ],
        ),
    ]
