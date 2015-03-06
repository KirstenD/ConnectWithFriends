from django.conf.urls import patterns, url
from rest_framework.authtoken import views as authtoken_views

from accounts import views

urlpatterns = patterns('',
    url(r'^create$', views.create, name='create'),
    url(r'^index$', views.index, name='index'),
    url(r'^login$', authtoken_views.obtain_auth_token, name='login'),
    url(r'^(?P<user_id>\d+)/$', views.detail, name='detail'),
    url(r'^whoami$', views.whoami, name='whoami'),
)
