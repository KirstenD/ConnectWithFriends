# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='active_player',
            field=models.ForeignKey(related_name='active_player', default=None, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='player2',
            field=models.ForeignKey(related_name='player2', default=None, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(related_name='winner', default=None, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
