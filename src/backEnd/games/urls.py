from django.conf.urls import patterns, url

from games import views

urlpatterns = patterns('',
    url(r'^start$', views.join, name='join'),
    url(r'^$', views.detail, name='detail'),
    url(r'^leave$', views.leave, name='leave'),
    url(r'^move/(?P<column_num>\d+)$', views.move, name='move'),
)
