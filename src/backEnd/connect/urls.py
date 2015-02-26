from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^chat/', include('chat.urls', namespace="chat")),
    url(r'^admin/', include(admin.site.urls)),
)
