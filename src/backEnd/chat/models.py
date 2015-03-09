from django.contrib.auth.models import User
from django.db import models

from games.models import Game


class GlobalMessage(models.Model):
    sender = models.ForeignKey(User)
    text = models.CharField(max_length=1024)
    pub_date = models.DateTimeField('date published')


class GameMessage(models.Model):
    sender = models.ForeignKey(User)
    text = models.CharField(max_length=1024)
    pub_date = models.DateTimeField('date published')
    game = models.ForeignKey(Game)
