# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guardias', '0004_auto_20150915_0923'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='listaguardias',
            unique_together=set([]),
        ),
    ]
