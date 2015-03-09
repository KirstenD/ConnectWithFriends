from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from accounts.serializers import UserSerializer
from friends.models import Follower


@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def index(request):
    """
    Get a list of all of your friends.
    """
    user = request.user
    friends = [f.followed for f in Follower.objects.filter(follower=user)]
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def add(request):
    """
    Add a user to your friends list.
    """
    if "id" not in request.data:
        return Response({"detail": "Must provide id."}, 400)
    try:
        friend = User.objects.get(pk=request.data["id"])
    except ObjectDoesNotExist:
        return Response({"detail": "Invalid user id."}, 400)
    user = request.user
    if friend == user:
        return Response({"detail": "Cannot add self."}, 400)
    friends = [f.followed for f in Follower.objects.filter(follower=user)]
    if friend not in friends:
        Follower(follower=user, followed=friend).save()
    friends = [f.followed for f in Follower.objects.filter(follower=user)]
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes((IsAuthenticated, ))
def delete(request):
    """
    Remove a friend from you friends list.
    """
    if "id" not in request.data:
        return Response({"detail": "Must provide id."}, 400)
    try:
        friend = User.objects.get(pk=request.data["id"])
    except ObjectDoesNotExist:
        return Response({"detail": "Invalid user id."}, 400)
    user = request.user
    try:
        Follower.objects.get(follower=user, followed=friend).delete()
    except ObjectDoesNotExist:
        return Response({"detail": "Specified user is not your friend."}, 400)
    return Response({}, 204)
