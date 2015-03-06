from rest_framework.serializers import ModelSerializer, SerializerMethodField

from games.models import Game


class GameSerializer(ModelSerializer):
    board = SerializerMethodField()
    is_active = SerializerMethodField()

    class Meta:
        model = Game
        fields = ("active_player",
                  "winner",
                  "stalemate",
                  "player1",
                  "player2",
                  "board",
                  "is_active")

    def get_board(self, obj):
        return obj.get_board

    def get_is_active(self, obj):
        return obj.is_active()
