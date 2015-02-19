from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from chat.models import GlobalChatMessage, PrivateChatMessage

def index(request):
    return HttpResponse(serializers.serialize("json", GlobalChatMessage.objects.all()))
