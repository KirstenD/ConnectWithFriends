from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from games.models import Game
from games.exceptions import GameFull, IllegalMove
from games.serializers import GameSerializer


@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def start(request):
    game = Game.join_or_create(request.user)
    return Response(GameSerializer(game).data)


@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def move(request, column_number):
    game = Game.active_game(request.user)
    if game is None:
        return Response({"detail": "Not currently in a game"}, 400)
    try:
        game.move(request.user, column_number)
    except IllegalMove as exception:
        return Response({"detail": str(exception)}, 400)
    return Response(GameSerializer(game).data, 200)


@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def detail(request):
    game = Game.active_game(request.user)
    if game is None:
        return Response({"detail": "Not currently in a game"}, 400)
    return Response(GameSerializer(game).data, 200)


@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def leave(request):
    game = Game.active_game(request.user)
    if game is None:
        return Response({"detail": "Not currently in a game"}, 400)
    game.leave(request.user)
    return Response(GameSerializer(game).data, 200)
