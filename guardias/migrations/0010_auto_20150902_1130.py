# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guardias', '0009_auto_20150902_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='periodovacaciones',
            name='vacaciones',
        ),
        migrations.DeleteModel(
            name='PeriodoVacaciones',
        ),
    ]
