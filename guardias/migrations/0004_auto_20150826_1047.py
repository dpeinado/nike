# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('guardias', '0003_auto_20150826_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guardia',
            name='doneby',
            field=models.ForeignKey(related_name='doneby', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
