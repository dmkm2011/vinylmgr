from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from reflibrary import views

urlpatterns = patterns('',
    url(r'^(?P<record_id>\d+)/$', views.record, name="r_record"),
    url(r'add/$', views.add_record, name="r_add_record"),
    url(r'adda/(?P<next>[0-9/A-Za-z]+)/$', views.add_artist, name="r_add_artist"),
    url(r'adda/$', views.add_artist, {'next':'/'}, name="r_add_artist_default"),
    url(r'adds/(?P<next>[0-9/A-Za-z]+)/$', views.add_soundtrack, name="r_add_soundtrack"),
    url(r'adds/$', views.add_soundtrack, {'next':'/'}, name="r_add_soundtrack_default"),
)
