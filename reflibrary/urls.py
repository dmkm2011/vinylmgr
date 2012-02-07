from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from reflibrary import views

urlpatterns = patterns('',
    url(r'^(?P<record_id>\d+)/$', views.record, name="r_record"),
)
