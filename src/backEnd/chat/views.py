from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from chat.models import GlobalMessage
from chat.serializers import GlobalMessageSerializer


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
