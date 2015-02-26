from django.contrib.auth.models import User
from rest_framework import serializers

from chat.models import GlobalMessage
from accounts.serializers import UserSerializer


class GlobalMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GlobalMessage
        fields = ('sender', 'text', 'pub_date')
