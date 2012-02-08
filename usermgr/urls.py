# decoupled from project vinylmgr/urls.py
from django.conf.urls.defaults import patterns, include, url
#from django.contrib.auth.views import *
#from vinylmgr.usermgr.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^login$', 'django.contrib.auth.views.login', name="auth_login", {'template_name': 'usermgr/login.html'})
)