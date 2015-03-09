from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from chat.models import GlobalMessage, GameMessage
from chat.serializers import GlobalMessageSerializer, GameMessageSerializer
from games.models import Game


@api_view(['GET'])
def global_message_list(request):
    """
    List all global chat messages, or create a global chat Message.
    """
    global_messages = GlobalMessage.objects.all()
    serializer = GlobalMessageSerializer(global_messages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def send_global_message(request):
    data = JSONParser().parse(request)
    data["sender"] = request.user.pk
    data["pub_date"] = timezone.now()
    serializer = GlobalMessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def game_message_list(request):
    """
    List all messages for the current game this user is in.
    """
    game = Game.current_game(request.user)
    if not game:
        return Response({"detail": "You are not in a game."}, 400)
    game_messages = GameMessage.objects.filter(game=game)
    game_messages = GameMessage.objects.all()
    serializer = GameMessageSerializer(game_messages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def send_game_message(request):
    game = Game.current_game(request.user)
    if not game:
        return Response({"detail": "You are not in a game."}, 400)
    data = JSONParser().parse(request)
    data["sender"] = request.user.pk
    data["pub_date"] = timezone.now()
    data["game"] = game.pk
    serializer = GameMessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
