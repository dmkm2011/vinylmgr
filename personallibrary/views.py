from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.views import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.utils.http import urlquote, base36_to_int
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_protect
from vinylmgr.personallibrary.forms import *
from vinylmgr.usermgr.models import *
from vinylmgr.reflibrary.models import Record
from vinylmgr.personallibrary.models import TrackedRecordList
from datetime import datetime

def personal_toggle_track(request):
    """
    Toggles whether a record is in a user's tracked list or not.
    """
    try:
        record_id = int(request.POST['record_id'])
    except (KeyError, ValueError):
        raise Http404
    record = get_object_or_404(Record, id=record_id)
    
    trackedrecord = TrackedRecordList.objects.filter(user=request.user.get_profile(), record=record)
    if len(trackedrecord) == 0:
        TrackedRecordList.objects.create(user=request.user.get_profile(), 
        record=record, tracked_time=datetime.now())
    else:
        trackedrecord[0].delete()
    
    # if request.is_ajax():
        # If the request is AJAX, return JSON representing the new count of
        # people who are attending the event.
    #    json = '{"created": %s, "count": %s}' % (created and 'true' or 'false', 
    #        event.attendees.all().count())
    #    return HttpResponse(json, mimetype='application/json')

    next = request.POST.get('next', '')
    #if not next:
    #    next = reverse('r_record')
    return HttpResponseRedirect(next)
    
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

