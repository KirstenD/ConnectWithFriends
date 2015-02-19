from django.contrib.auth.models import User
from django.db import models

class GlobalChatMessage(models.Model):
    sender = models.ForeignKey(User)
    text = models.CharField(max_length=1024)
    pub_date = models.DateTimeField('date published')

class PrivateChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sender')
    recipient = models.ForeignKey(User, related_name='recipient')
    text = models.CharField(max_length=1024)
    pub_date = models.DateTimeField('date published')
