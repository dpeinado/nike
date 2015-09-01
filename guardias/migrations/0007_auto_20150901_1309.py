# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('guardias', '0006_auto_20150827_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodoVacaciones',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('comienzo', models.DateField()),
                ('final', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='VacacionesAnuales',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('año', models.IntegerField()),
                ('dias_de_vacaciones', models.IntegerField(default=22)),
                ('persona', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='periodovacaciones',
            name='vacaciones',
            field=models.ForeignKey(to='guardias.VacacionesAnuales'),
        ),
    ]
