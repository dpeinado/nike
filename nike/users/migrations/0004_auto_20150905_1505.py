# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import nike.users.managers
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150905_1458'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('guardias', nike.users.managers.MyUserManager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
