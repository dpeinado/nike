# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('guardias', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vacacionesanuales',
            name='persona',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='guardia',
            name='ausencias',
            field=models.ManyToManyField(related_name='vacaciones', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='guardia',
            name='centro',
            field=models.ForeignKey(to='guardias.Centro'),
        ),
        migrations.AddField(
            model_name='guardia',
            name='doneby',
            field=models.ForeignKey(related_name='doneby', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='guardia',
            name='owner',
            field=models.ForeignKey(related_name='owner', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='centro',
            name='organizacion',
            field=models.ForeignKey(to='guardias.Organizacion', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='centro',
            name='supervisor',
            field=models.ForeignKey(related_name='supervisor', to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
    ]
