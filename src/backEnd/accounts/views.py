from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status


@api_view(["PUT", "POST"])
def create(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    if not username or not password:
        data = {"details": "Username or password not specified."}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        data = {"details": "Username already taken."}
        return Response(data, status=status.HTTP_409_CONFLICT)
    user = User.objects.create_user(username, '', password)
    if not user:
        data = {"details": "Account creation failed"}
        return Response(data, status=status.HTTP_409_CONFLICT)
    return Response({"token": str(user.auth_token)})


@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def whoami(request):
    """
    TODO: use serializer
    """
    data = {"username": request.user.username}
    return Response(data)
