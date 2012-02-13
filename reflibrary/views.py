from django.utils.translation import ugettext as _
from django.contrib.auth.views import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from reflibrary.models import *
from reflibrary.forms import *

def browse(request):
    """
    Renders a list of ``Record`` instances
    """
    
    #records = Record.objects.all().order_by('-modified_date').distinct()[:8]
    records = Record.objects.all().order_by('-modified_date').distinct()
    context = {
        'records': records
    }
    return render_to_response(
        'reflibrary/browse.html',
        context,
        context_instance = RequestContext(request)
    )

def record(request, record_id):
    """
    Renders a single record
    """
    r = get_object_or_404(Record, id=record_id)
    featuring = RecordFeaturing.objects.filter(record = r)
    tracks = r.soundtrack.all()
    for s in tracks:
        l = SoundTrackFeaturing.objects.filter(soundtrack = s)
        if len(l) > 0:
            s.artist = l[0].artist
        else:
            s.artist = None
    recommends = Record.objects.all()[:4]
    if request.user.is_authenticated():
        if len(request.user.get_profile().trackedrecordlist_set.filter(record__id=record_id)) > 0:
            tracked = 1
        else:
            tracked = -1
    else:
        tracked = 0
    return render_to_response(
        'reflibrary/record.html',
        {'record': r,
         'featuring': featuring,
         'tracks': tracks,
         'tracked': tracked,
         'recommends': recommends},
        context_instance = RequestContext(request)
    )

@login_required
def add_record(request, template_name='reflibrary/addrecord_form.html', 
           add_form=RecordCreationForm,
           post_redirect=None):
    #if post_redirect is None:
    #    post_redirect = reverse('vinylmgr.usermgr.views.signup_done')
    if request.method == "POST":
        form = add_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_redirect)
    else:
        form = add_form()
    return render_to_response(template_name, {'form': form}, 
                              context_instance=RequestContext(request))

def add_obj(request, modelForm, model, template, id_field, next):
    if request.method == "POST":
        next = request.POST['next']
        
        if 'cancel' in request.POST:
            return HttpResponseRedirect(next)

        obj_id = request.POST[id_field]            
        if obj_id == 'None':
            # this artist is new
            form = modelForm(request.POST)
        else:
            obj = get_object_or_404(model, id = obj_id)
            form = modelForm(request.POST, instance = obj)
        
        if form.is_valid():
            form.save()  
            # if 'saveAndEdit' in request.POST:
                # do nothing
            if 'saveAndAddMore' in request.POST:
                form = modelForm()
            elif 'save' in request.POST:
                return HttpResponseRedirect(next)
    else:
        form = modelForm()
    return render_to_response(template,
                            {'form': form, 'next': next}, 
                              context_instance=RequestContext(request))
                              
@login_required
def add_artist(request, next=None):
    return add_obj(request, ArtistCreationForm, 
        Artist, 'reflibrary/addartist_form.html', 'artist_id', next)
                              
@login_required
def edit_artist(request, artist_id, next=None):
    artist = get_object_or_404(Artist, id=artist_id)
        
    if request.method == 'POST':
        next = request.POST['next']
        form = ArtistCreationForm(data=request.POST, files=request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(next)
    else:
        p_initial = {'name': artist.name,
                  'homepage': artist.homepage,
                  'bio': artist.bio}
        form = ArtistCreationForm(initial=p_initial, instance=artist)
    return render_to_response(template_name,
                          { 'form': form},
                          context_instance=RequestContext(request))
                              
@login_required
def add_soundtrack(request, next=None):
        return add_obj(request, SoundTrackCreationForm, 
        SoundTrack, 'reflibrary/addsoundtrack_form.html', 'soundtrack_id', next)