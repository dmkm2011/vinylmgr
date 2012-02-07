# decoupling to app usermgr/urls.py (PLUG & PLAY)
# This also imports the include function
from django.conf.urls.defaults import *
from django.contrib.auth.views import *
from vinylmgr.usermgr.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^usermgr/', include('usermgr.urls')), #can change path as your wish
#   url(r'^admin/', include(admin.site.urls)),
    
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'usermgr/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'usermgr/logged_out.html'}),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'usermgr/password_change_form.html'}),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'usermgr/password_change_done.html'}),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',{'template_name': 'usermgr/password_reset_form.html','email_template_name': 'usermgr/password_reset_email.html'}),
    url(r'^password_reset/done/$','django.contrib.auth.views.password_reset_done',{'template_name': 'usermgr/password_reset_done.html'}),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'usermgr/password_reset_confirm.html'}),
    url(r'^reset/done/$','django.contrib.auth.views.password_reset_complete', {'template_name': 'usermgr/password_reset_complete.html'}),
    url(r'^signup/$', 'vinylmgr.usermgr.views.signup',{'template_name': 'usermgr/signup_form.html','email_template_name': 'usermgr/signup_email.html'}),
    url(r'^signup/done/$','vinylmgr.usermgr.views.signup_done',{'template_name': 'usermgr/signup_done.html'}),
    url(r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','vinylmgr.usermgr.views.signup_confirm'),
    url(r'^signup/complete/$','vinylmgr.usermgr.views.signup_complete', {'template_name': 'usermgr/signup_complete.html'}),
)
