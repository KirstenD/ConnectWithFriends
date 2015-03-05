from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    follower = models.ForeignKey(User, related_name="follower")
    followed = models.ForeignKey(User, related_name="followed")

    def __unicode__(self):
        return str(self.follower) + " -> " + str(self.followed)
