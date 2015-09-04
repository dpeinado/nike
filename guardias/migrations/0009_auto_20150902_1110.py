# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guardias', '0008_guardia_ausencias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodovacaciones',
            name='vacaciones',
            field=models.ForeignKey(related_name='periodos', to='guardias.VacacionesAnuales'),
        ),
    ]
