# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guardias', '0002_auto_20150907_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardia',
            name='fijada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='guardia',
            name='pivote',
            field=models.BooleanField(default=False),
        ),
    ]
