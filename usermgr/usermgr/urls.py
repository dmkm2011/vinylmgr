# decoupled from project vinylmgr/urls.py
from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('usermgr.views',
    url(r'^$', 'homepage'),
    url(r'^homepage', 'homepage'),
)