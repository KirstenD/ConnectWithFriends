from django.conf.urls import patterns, url

from games import views

urlpatterns = patterns('',
    url(r'^start$', views.start, name='start'),
    url(r'^detail$', views.detail, name='detail'),
    url(r'^leave$', views.leave, name='leave'),
    url(r'^move/(?P<column_number>\d+)$', views.move, name='move'),
)
