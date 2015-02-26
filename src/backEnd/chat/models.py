from django.contrib.auth.models import User
from django.db import models

class GlobalMessage(models.Model):
    sender = models.ForeignKey(User)
    text = models.CharField(max_length=1024)
    pub_date = models.DateTimeField('date published')
