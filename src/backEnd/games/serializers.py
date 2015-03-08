from rest_framework.serializers import ModelSerializer, SerializerMethodField

from games.models import Game


class GameSerializer(ModelSerializer):
    board = SerializerMethodField()

    class Meta:
        model = Game
        fields = ("turn",
                  "winner",
                  "stalemate",
                  "player1",
                  "player2",
                  "board")

    def get_board(self, obj):
        board = obj.get_board()
        serialized_board = []
        for row in board:
            player_ids = [player.pk if player else None for player in row]
            serialized_board.append(player_ids)
        return serialized_board
