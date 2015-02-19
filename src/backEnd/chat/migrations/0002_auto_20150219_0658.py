# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalChatMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=1024)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrivateChatMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=1024)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('recipient', models.ForeignKey(related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='globalchatmessagemodel',
            name='sender',
        ),
        migrations.DeleteModel(
            name='GlobalChatMessageModel',
        ),
        migrations.RemoveField(
            model_name='privatechatmessagemodel',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='privatechatmessagemodel',
            name='sender',
        ),
        migrations.DeleteModel(
            name='PrivateChatMessageModel',
        ),
    ]
