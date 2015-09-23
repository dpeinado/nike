# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guardias', '0005_auto_20150915_0926'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='listaguardias',
            unique_together=set([('centro', 'tipo', 'orden')]),
        ),
    ]
