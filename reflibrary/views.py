from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from reflibrary.models import Record

def browse(request):
    """
    Renders a list of ``Record`` instances
    """
    
    records = Record.objects.all()
    #if request.user.is_authenticated():
        #following = list(request.user.following_set.all().values_list('to_user', 
        #    flat=True))
        
    #else:
        #following = None
    records = records.order_by('-title', '-matrix_number').distinct()
    context = {
        'records': records
    }
    return render_to_response(
        'reflibrary/browse.html',
        context,
        context_instance = RequestContext(request)
    )
