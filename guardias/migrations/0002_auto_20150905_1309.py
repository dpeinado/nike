# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('guardias', '0001_initial'),
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
            name='doneby',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='doneby'),
        ),
        migrations.AddField(
            model_name='guardia',
            name='owner',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='owner'),
        ),
        migrations.AddField(
            model_name='centro',
            name='organizacion',
            field=models.ForeignKey(null=True, blank=True, to='guardias.Organizacion'),
        ),
        migrations.AddField(
            model_name='centro',
            name='supervisor',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='supervisor'),
        ),
    ]
