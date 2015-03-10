from rest_framework import serializers

from chat.models import GlobalMessage, GameMessage


class GlobalMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    display_time = serializers.SerializerMethodField()

    class Meta:
        model = GlobalMessage
        fields = ('sender', 'text', 'pub_date', 'sender_name', 'display_time')

    def get_sender_name(self, obj):
        return obj.sender.username
    
    def get_display_time(self, obj):
        return obj.pub_date.strftime("%B %d, %I:%M:%S %p")


class GameMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    display_time = serializers.SerializerMethodField()

    class Meta:
        model = GameMessage
        fields = ('sender', 'text', 'pub_date', 'game', 'sender_name', 'display_time')

    def get_sender_name(self, obj):
        return obj.sender.username
    
    def get_display_time(self, obj):
        return obj.pub_date.strftime("%B %d, %I:%M:%S %p")
