from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from games.models import Game
from games.exceptions import GameFull
from games.serializers import GameSerializer


@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def start(request):
    if any(game.is_active for game in Game.get_games(request.user)):
        return Response({"detail": "Already in game."}, 400)
    available_games = Game.objects.filter(player2=None)
    if available_games.count():
        try:
            available_games[0].join(request.user)
            game = available_games[0]
            return Response(GameSerializer(game).data)
        except GameFull:
            pass
    game = Game.create_game(request.user)
    return Response(GameSerializer(game).data)
