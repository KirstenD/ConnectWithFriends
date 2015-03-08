from django.conf.urls import patterns, url

from games import views

urlpatterns = patterns('',
    url(r'^start$', views.start, name='start'),
    url(r'^detail$', views.detail, name='detail'),
    url(r'^forfeit$', views.forfeit, name='forfeit'),
    url(r'^move/(?P<column_number>\d+)$', views.move, name='move'),
)
