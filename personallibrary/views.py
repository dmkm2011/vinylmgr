# Create your views here.


from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.views import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from vinylmgr.personallibrary.forms import UserCreationForm
from vinylmgr.personallibrary.forms import PlaylistCreationForm
from vinylmgr.personallibrary.forms import SharePlaylistCreationForm
from vinylmgr.personallibrary.forms import ViewEditPlaylistCreationForm
from vinylmgr.usermgr.models import *
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.utils.http import urlquote, base36_to_int
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_protect


def personal_library(request,template_name='personallibrary/personallibrary_form.html'):
    return render_to_response(template_name)	
	
def personal_library_create(request,template_name='personallibrary/personallibrary_create.html',create_form=PlaylistCreationForm,token_generator=default_token_generator,post_create_redirect=None):
	   	
	form = create_form()
	return render_to_response(template_name, {'form': form,},context_instance=RequestContext(request))	

def create_done(request, template_name='personallibrary/create_done.html'):
    return render_to_response(template_name, 
                              context_instance=RequestContext(request))	
	
def personal_library_viewedit(request,template_name='personallibrary/personallibrary_viewedit.html',viewedit_form=ViewEditPlaylistCreationForm,token_generator=default_token_generator):
	
	form = viewedit_form()
	return render_to_response(template_name, {'form': form,},context_instance=RequestContext(request))	
	
def personal_library_share(request,template_name='personallibrary_shareplaylist.html',share_form=SharePlaylistCreationForm,token_generator=default_token_generator):
		
	form = share_form()
	return render_to_response(template_name, {'form': form,},context_instance=RequestContext(request))		

