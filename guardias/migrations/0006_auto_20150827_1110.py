# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guardias', '0005_auto_20150827_0706'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guardia',
            options={'ordering': ['id']},
        ),
    ]
