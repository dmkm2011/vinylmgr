from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.views import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from vinylmgr.usermgr.forms import UserCreationForm, ProfileEditForm
from vinylmgr.usermgr.models import *
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.utils.http import urlquote, base36_to_int
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_protect
#from profiles import views as profile_views
#from usermgr.forms import ProfileEditForm 
 
@csrf_protect
def signup(request, template_name='usermgr/signup.html', 
           email_template_name='usermgr/password_signup_email.html',
           signup_form=UserCreationForm,
           token_generator=default_token_generator,
           post_signup_redirect=None):
    if post_signup_redirect is None:
        post_signup_redirect = reverse('vinylmgr.usermgr.views.signup_done')
    if request.method == "POST":
        form = signup_form(request.POST)
        if form.is_valid():
            opts = {}
            opts['use_https'] = request.is_secure()
            opts['token_generator'] = token_generator
            opts['email_template_name'] = email_template_name
            if not Site._meta.installed:
                opts['domain_override'] = Site(request).domain
            form.save(**opts)
            return HttpResponseRedirect(post_signup_redirect)
    else:
        form = signup_form()
    return render_to_response(template_name, {'form': form,}, 
                              context_instance=RequestContext(request))

def signup_done(request, template_name='usermgr/password_signup_done.html'):
    return render_to_response(template_name, 
                              context_instance=RequestContext(request))

def signup_confirm(request, uidb36=None, token=None,
                   token_generator=default_token_generator,
                   post_signup_redirect=None):
    assert uidb36 is not None and token is not None #checked par url
    if post_signup_redirect is None:
        post_signup_redirect = reverse('vinylmgr.usermgr.views.signup_complete')
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, id=uid_int)
    context_instance = RequestContext(request)

    if token_generator.check_token(user, token):
        context_instance['validlink'] = True
        user.is_active = True
        user.save()
    else:
        context_instance['validlink'] = False
    return HttpResponseRedirect(post_signup_redirect)

def signup_complete(request, template_name='usermgr/password_signup_complete.html'):
    return render_to_response(template_name, 
                              context_instance=RequestContext(request, 
                                                              {'login_url': settings.LOGIN_URL}))

def password_reset(request):
	"""
	django.contrib.auth.views.password_reset view (forgotten password)
	"""
	if not request.user.is_authenticated():
		return django.contrib.auth.views.password_reset(request,
                          template_name='usermgr/password_reset_form.html',
                          email_template_name= 'usermgr/password_reset_email.html',
                          post_reset_redirect='/usermgr/password_reset/done/')
	else:
		return HttpResponseRedirect("/user/")
    
@login_required
def profile(request, username=None):
    """
    Renders information about a single user's profile.
    """
    user = request.user.get_profile()
    context = {
        'user': user,
    }
    return render_to_response(
        'usermgr/profile.html',
        context,
        context_instance = RequestContext(request))
        
def profile_edit(request, template_name='usermgr/edit_profile.html', profile_edit_form=ProfileEditForm,):
    form = profile_edit_form(request.POST)
    if form.is_valid():
       form.save()
    #return profile_views.edit_profile(request, form_class=ProfileEditForm)
    return render_to_response(template_name, {'form': form,}, context_instance=RequestContext(request))