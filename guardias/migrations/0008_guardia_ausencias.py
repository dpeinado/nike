# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('guardias', '0007_auto_20150901_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardia',
            name='ausencias',
            field=models.ManyToManyField(related_name='vacaciones', to=settings.AUTH_USER_MODEL),
        ),
    ]
