# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stalemate', models.BooleanField(default=False)),
                ('active_player', models.ForeignKey(related_name='active_player', blank=True, to=settings.AUTH_USER_MODEL)),
                ('player1', models.ForeignKey(related_name='player1', to=settings.AUTH_USER_MODEL)),
                ('player2', models.ForeignKey(related_name='player2', blank=True, to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(related_name='winner', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField()),
                ('column', models.ForeignKey(to='games.Column')),
                ('player', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='column',
            name='game',
            field=models.ForeignKey(to='games.Game'),
            preserve_default=True,
        ),
    ]
