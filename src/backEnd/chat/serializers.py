from rest_framework import serializers

from chat.models import GlobalMessage, GameMessage


class GlobalMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalMessage
        fields = ('sender', 'text', 'pub_date')


class GameMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMessage
        fields = ('sender', 'text', 'pub_date', 'game')
