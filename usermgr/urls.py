# decoupled from project vinylmgr/urls.py
from django.conf.urls.defaults import patterns, include, url
from vinylmgr.usermgr.forms import ProfileEditForm
#from django.contrib.auth.views import *
#from vinylmgr.usermgr.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'usermgr/login.html'}, name="auth_login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'usermgr/logout.html'}, name="auth_logout"),
    url(r'^pchange/$', 'django.contrib.auth.views.password_change', {'template_name': 'usermgr/password_change_form.html'}),
    url(r'^pchange/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'usermgr/password_change_done.html'}),
    url(r'^preset/$', 'django.contrib.auth.views.password_reset',{'template_name': 'usermgr/password_reset_form.html','email_template_name': 'usermgr/password_reset_email.html'}),
    url(r'^preset/done/$','django.contrib.auth.views.password_reset_done',{'template_name': 'usermgr/password_reset_done.html'}),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'usermgr/password_reset_confirm.html'}),
    url(r'^reset/done/$','django.contrib.auth.views.password_reset_complete', {'template_name': 'usermgr/password_reset_complete.html'}),
    url(r'^signup/$', 'vinylmgr.usermgr.views.signup',{'template_name': 'usermgr/signup_form.html','email_template_name': 'usermgr/signup_email.html'}, name="registration_register"),
    url(r'^signup/done/$','vinylmgr.usermgr.views.signup_done',{'template_name': 'usermgr/signup_done.html'}),
    url(r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','vinylmgr.usermgr.views.signup_confirm'),
    url(r'^signup/complete/$','vinylmgr.usermgr.views.signup_complete', {'template_name': 'usermgr/signup_complete.html'}),
    url(r'^profile/$','vinylmgr.usermgr.views.profile', name="profile"),
    url(r'^profile/edit$','vinylmgr.usermgr.views.profile_edit',{'form_class': ProfileEditForm}, name="profile_edit"),
)