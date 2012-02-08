# decoupling to app usermgr/urls.py (PLUG & PLAY)
# This also imports the include function
from django.conf.urls.defaults import *
from django.contrib.auth.views import *
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'vinylmgr.reflibrary.views.browse', name="index"),
    url(r'^r/', include('vinylmgr.reflibrary.urls')),
    
    # lyon added usermgr
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'usermgr/login.html'}, name="auth_login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'usermgr/logout.html'}, name="auth_logout"),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'usermgr/password_change_form.html'}),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'usermgr/password_change_done.html'}),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',{'template_name': 'usermgr/password_reset_form.html','email_template_name': 'usermgr/password_reset_email.html'}),
    url(r'^password_reset/done/$','django.contrib.auth.views.password_reset_done',{'template_name': 'usermgr/password_reset_done.html'}),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'usermgr/password_reset_confirm.html'}),
    url(r'^reset/done/$','django.contrib.auth.views.password_reset_complete', {'template_name': 'usermgr/password_reset_complete.html'}),
    url(r'^signup/$', 'vinylmgr.usermgr.views.signup',{'template_name': 'usermgr/signup_form.html','email_template_name': 'usermgr/signup_email.html'}, name="registration_register"),
    url(r'^signup/done/$','vinylmgr.usermgr.views.signup_done',{'template_name': 'usermgr/signup_done.html'}),
    url(r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','vinylmgr.usermgr.views.signup_confirm'),
    url(r'^signup/complete/$','vinylmgr.usermgr.views.signup_complete', {'template_name': 'usermgr/signup_complete.html'}),
    url(r'^accounts/profile/$','vinylmgr.usermgr.views.profile'),
    
    # lyon added personallibrary
    url(r'^create_done/$', 'vinylmgr.personallibrary.views.create_done',{'template_name': 'personallibrary/personallibrary_create_done.html'}),
    url(r'^personal_library/', include('vinylmgr.personallibrary.urls')),
    
    # these URLs are not working, just reservations for base.html template
    url(r'^personal$', 'vinylmgr.views.index', name="personallib"),
    url(r'^about/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/about.html'}, name="about"),
    url(r'^help/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/help.html'}, name="help"),
    ##############################################
    	# Acknowledgement
		url(r'^acknowledgement/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/acknowledgement.html'}, name="acknowledgement"),
		##############################################
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

    # Start Lyon part
    # Commented because it causes TemplateSyntaxError: Could not import vinylmgr.usermgr.views. Error was: No module named views
    
    #url(r'^usermgr/', include('usermgr.urls')), #can change path as your wish
    
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'usermgr/login.html'}),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'usermgr/logged_out.html'}),
    #url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'usermgr/password_change_form.html'}),
    #url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'usermgr/password_change_done.html'}),
    #url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',{'template_name': 'usermgr/password_reset_form.html','email_template_name': 'usermgr/password_reset_email.html'}),
    #url(r'^password_reset/done/$','django.contrib.auth.views.password_reset_done',{'template_name': 'usermgr/password_reset_done.html'}),
    #url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'usermgr/password_reset_confirm.html'}),
    #url(r'^reset/done/$','django.contrib.auth.views.password_reset_complete', {'template_name': 'usermgr/password_reset_complete.html'}),
    #url(r'^signup/$', 'vinylmgr.usermgr.views.signup',{'template_name': 'usermgr/signup_form.html','email_template_name': 'usermgr/signup_email.html'}),
    #url(r'^signup/done/$','vinylmgr.usermgr.views.signup_done',{'template_name': 'usermgr/signup_done.html'}),
    #url(r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','vinylmgr.usermgr.views.signup_confirm'),
    #url(r'^signup/complete/$','vinylmgr.usermgr.views.signup_complete', {'template_name': 'usermgr/signup_complete.html'}),
)
