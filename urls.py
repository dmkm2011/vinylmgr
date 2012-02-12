from django.conf.urls.defaults import *
from django.contrib.auth.views import *
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'vinylmgr.reflibrary.views.browse', name="index"),
    url(r'^r/', include('vinylmgr.reflibrary.urls')),
    url(r'^u/', include('vinylmgr.usermgr.urls')),
    url(r'^p/', include('vinylmgr.personallibrary.urls')),
    
    # misc pages
    url(r'^about/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/about.html'}, name="about"),
    url(r'^help/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/help.html'}, name="help"),
    #url(r'^search/$', 'django.views.generic.simple.direct_to_template', 
     #   {'template': 'misc/search.html'}, name="search"),
    url(r'^search/$', 'views.search', name="search"),
	url(r'^ack/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/acknowledgement.html'}, name="acknowledgement"),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
