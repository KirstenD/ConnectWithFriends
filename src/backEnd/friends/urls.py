from django.conf.urls import patterns, url

from friends import views

urlpatterns = patterns('',
    url(r'^index$', views.index, name='index'),
    url(r'^add$', views.add, name='add'),
    url(r'^delete/(?P<user_id>\d+)$', views.delete, name='delete'),
)
