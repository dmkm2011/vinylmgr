from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from reflibrary.models import SoundTrack
from reflibrary.models import Record
from reflibrary.models import Style
from reflibrary.models import Genre
from reflibrary.models import Artist
from reflibrary.models import Role
#####################################Search####
import re

from django.db.models import Q

def index(request):
    """
    A proxy view for either the ``direct_to_template`` generic view, or to
    a redirect, depending on whether the user is authenticated.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('ev_tonight'))
    return direct_to_template(request, template='index.html')
    
# Added a new view for search	
def search(request):
    if request.method == "GET":
        return render_to_response('misc/search.html',
        {}, context_instance=RequestContext(request))
    elif request.method == "POST":
        Listbox = request.POST.get('mydropdown')
        terms = request.POST.get('q')
        stories = ''
        if Listbox == "SoundTrack":
            stories = SoundTrack.objects.all()
            q = Q(name__icontains=terms)
        elif Listbox == "Record":
            stories = Record.objects.all()
            q = Q(title__icontains=terms)
        elif Listbox == "Style":
            stories = Style.objects.all()
            q = Q(name__icontains=terms)
        elif Listbox == "Genre":
            stories = Genre.objects.all()
            q = Q(name__icontains=terms)
        elif Listbox == "Artist":
            print "Artist"
            stories = Artist.objects.all()
            q = Q(name__icontains=terms)
        elif Listbox == "Role":
            stories = Role.objects.all()
            q = Q(name__icontains=terms)
        
        stories = stories.filter(q).values        
        
        return render_to_response('misc/search.html',{ 'query_string': stories, 'found_entries': Listbox },context_instance=RequestContext(request))