from django.conf.urls import patterns, url

from chat import views

urlpatterns = patterns('',
    url(r'^index$', views.global_message_list, name='index'),
    url(r'^send$', views.send_global_message, name='send'),
    url(r'^game/index$', views.game_message_list, name='game_index'),
    url(r'^game/send$', views.send_game_message, name='game_send'),
)
