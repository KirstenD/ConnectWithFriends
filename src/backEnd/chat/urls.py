from django.conf.urls import patterns, url

from chat import views

urlpatterns = patterns('',
    url(r'^index$', views.global_message_list, name='index'),
    url(r'^global$', views.send_global_message, name='detail'),
)
