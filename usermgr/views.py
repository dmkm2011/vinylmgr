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
from PIL import Image as PImage
from os.path import join as pjoin
from django import forms
 
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
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["user",]
    
@login_required    
def profile(request, username=None):
    """
    Renders information about a single user's profile.  This includes
    information about who follows them, who they follow, mutual followers, the
    latest events created, and whether the currently logged in user is a friend
    of the user to render.
    """
    user = request.user.get_profile()
    
    context = {
        'User': user,
    }
    return render_to_response(
        'usermgr/profile.html',
        context,
        context_instance = RequestContext(request)
    )
    
def profile_edit(request, form_class=None, success_url=None, template_name='usermgr/edit_profile.html'):
    #try:
    profile_obj = request.user.get_profile()
    #    img = None
    #except ObjectDoesNotExist:
    #    return HttpResponseRedirect(reverse('registration_register'))
    success_url='/u/profile/'
    if form_class is None:
        form_class = ProfileEditForm
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(success_url)
    #       # resize and save image under same filename
    #        imfn = pjoin(MEDIA_ROOT, profile.avatar.name)
    #        im = PImage.open(imfn)
    #        im.thumbnail((160,160), PImage.ANTIALIAS)
    #        im.save(imfn, "JPEG")
    #        #return HttpResponseRedirect(success_url)
    else:
        form = form_class(instance=profile_obj)
    
    #if profile_obj.avatar:
    #    img = "/media/" + profile_obj.avatar.name
    
    #if extra_context is None:
    #    extra_context = {}
    context = RequestContext(request)
    
    
    #for key, value in extra_context.items():
    #    context[key] = callable(value) and value() or value
    
    return render_to_response(template_name,
                              { 'form': form,
                                'profile': profile_obj, },
                              context_instance=context,)
#profile_edit = login_required(profile_edit)

#return render_to_response("forum/profile.html", add_csrf(request, pf=pf, img=img))