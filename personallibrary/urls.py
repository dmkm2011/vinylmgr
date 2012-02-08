from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from personallibrary import views

urlpatterns = patterns('',
    url(r'^$', 'vinylmgr.personallibrary.views.personal_library',{'template_name': 'personallibrary/personallibrary_form.html'}),
    url(r'^create/$', 'vinylmgr.personallibrary.views.personal_library_create',{'template_name': 'personallibrary/personallibrary_create.html'}, name="playlist_create"),
    url(r'^viewedit/$', 'vinylmgr.personallibrary.views.personal_library_viewedit',{'template_name': 'personallibrary/personallibrary_viewedit.html'},name="playlist_viewedit"),
    url(r'^share/$', 'vinylmgr.personallibrary.views.personal_library_share',{'template_name': 'personallibrary/personallibrary_shareplaylist.html'},name="playlist_share"),
    
)
