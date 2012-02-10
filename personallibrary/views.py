# Create your views here.


from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.views import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from vinylmgr.personallibrary.forms import UserCreationForm
from vinylmgr.personallibrary.forms import *
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
	
def personal_library_create(request,template_name='personallibrary/personallibrary_create.html',token_generator=default_token_generator,post_create_redirect=None):
	
	if request.method == "POST":
		f = create_form(request.POST)   	
		if not f.is_valid():			
			return render_to_response("personallibrary/personallibrary_create.html",{"f":f})
		else:			
			f.save()
			return render_to_response("personallibrary/personallibrary_create_done.html",{"f":f})
	
	f = create_form()	
	return render_to_response('personallibrary/personallibrary_create.html', {'f': f,},context_instance=RequestContext(request))		
		
def create_done(request, template_name='personallibrary/personallibrary_create_done.html'):
    return render_to_response(template_name, 
                              context_instance=RequestContext(request))	
	
def personal_library_viewedit(request,template_name = 'Personallibrary/personallibrary_viewedit.html'):		
	if request.method == "POST":
		f = viewedit_form(request.POST) 
		f.display()
		if not f.is_valid():
			return render_to_response("personallibrary/personallibrary_viewedit.html",{"f":f})
		else:
			f.txtchoose()
			f.save()
			return render_to_response("personallibrary/personallibrary_create_done.html",{"f":f})
	f = viewedit_form()
	return render_to_response('personallibrary/personallibrary_viewedit.html', context_instance=RequestContext(request))		
	
def personal_library_share(request,template_name='personallibrary_shareplaylist.html',share_form=SharePlaylistCreationForm,token_generator=default_token_generator):
		
	form = share_form()
	return render_to_response(template_name, {'form': form,},context_instance=RequestContext(request))		

