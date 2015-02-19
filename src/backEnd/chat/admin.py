from django.contrib import admin
from chat.models import GlobalChatMessage, PrivateChatMessage

admin.site.register(GlobalChatMessage)
admin.site.register(PrivateChatMessage)
