from django.utils.translation import ugettext as _
from django.contrib.auth.views import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from reflibrary.models import Record, RecordFeaturing, SoundTrackFeaturing
from reflibrary.forms import RecordCreationForm

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
    return render_to_response(template_name, {'form': form,}, 
                              context_instance=RequestContext(request))
