from django.contrib.sites.models import Site
from vinylmgr.personallibrary.models import *
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36
from django.template import Context, loader
from django import forms
from django.core.mail import send_mail

class create_form(forms.ModelForm):
	#playlistname = forms.CharField(label="Playlist name")
	#playlistdiscription = forms.CharField(label="Discription")		
	
	class Meta:
		model = Playlist
		
	def save(self, commit=True, domain_override=None,             
             use_https=False, token_generator=default_token_generator):
		Playlist = super(create_form, self).save(commit=False)
		Playlist.is_active = False
		Playlist.save()	



class viewedit_form(forms.ModelForm):

	class Meta:
		model = Playlist
		
	def display(self,commit=True, domain_override=None,             
             use_https=False, token_generator=default_token_generator):
	
		ROLE_CHOICES=(
		(0, 'Name'),
		(1, 'Description'),
		(2, 'Created time'),
		(3, 'Privecy'),
		(4, 'Published')
		)
		edit = models.IntegerField('Playlist information to change', choices=ROLE_CHOICES)   
		return edit	
			
	def txtchoose(self,commit=True, domain_override=None,             
             use_https=False, token_generator=default_token_generator):
	     
		if ViewEditPlaylist.edit == 'Name':
			name = models.CharField('Playlist name', max_length = 100)
		elif display.edit == 'Description': 				
			description = models.CharField('Playlist description', max_length = 200)
		elif display.edit == 'Created time': 				
			created_time = models.DateTimeField()
		elif display.edit == 'Privacy': 							
			privacy = models.IntegerField(choices=PRIVACY_CHOICES)
		elif display.edit == 'Published': 					
			published = models.IntegerField(choices=PUBLISH_CHOICES)
			
	def save(self, commit=True, domain_override=None,             
             use_https=False, token_generator=default_token_generator):
		Playlist = super(viewedit_form, self).save(commit=False)
		if display.edit == 'Name':
			edit_name = Playlist.object.get(name = txtchoose.name)
			edit_name.name = txtchoose.newname
		elif display.edit == 'Desciption':		
			edit_name = Playlist.object.get(name = txtchoose.description)
			edit_name.description = txtchoose.newdescription
		elif display.edit == 'Created time': 				
			edit_name = Playlist.object.get(name = txtchoose.create_time)
			edit_name.created_time = txtchoose.newcreated_time
		elif display.edit == 'Privacy': 							
			edit_name = Playlist.object.get(privacy = txtchoose.privacy)
			edit_name.privacy = txtchoose.newprivacy
		elif display.edit == 'Published': 					
			edit_name = Playlist.object.get(name = txtchoose.published)
			edit_name.published = txtchoose.newpublished
		Playlist.is_active = False
		Playlist.save()			
	



class UserCreationForm(forms.ModelForm):
    username = forms.RegexField(label="Username", max_length=30, regex=r'^[\w.@+-]+$',
                                help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
                                error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
                                help_text = "Enter the same password as above, for verification.")
    email1 = forms.EmailField(label="Email", max_length=75)
    email2 = forms.EmailField(label="Email confirmation", max_length=75,
                              help_text = "Enter your email address again. A confirmation email will be sent to this address.")
    firstname = forms.CharField(label="First name*", widget=forms.TextInput)
    lastname = forms.CharField(label="Last name", widget=forms.TextInput)
    
    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2
    
    def clean_email1(self):
        email1 = self.cleaned_data["email1"]
        users_found = User.objects.filter(email__iexact=email1)
        if len(users_found) >= 1:
            raise forms.ValidationError("A user with that email already exist.")
        return email1

    def clean_email2(self):
        email1 = self.cleaned_data.get("email1", "")
        email2 = self.cleaned_data["email2"]
        if email1 != email2:
            raise forms.ValidationError("The two email fields didn't match.")
        return email2

    def save(self, commit=True, domain_override=None,
             email_template_name='registration/signup_email.html',
             use_https=False, token_generator=default_token_generator):
        user = super(UserCreationForm, self).save(commit=False)
        ######NOT SURE############
        user.first_name = firstname 
        user.last_name = lastname
        ##########################
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email1"]
        user.is_active = False
        if commit:
            user.save()
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': int_to_base36(user.id),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': use_https and 'https' or 'http',
            }
        send_mail("Confirmation link sent on %s" % site_name,
                  t.render(Context(c)), 'peyman.gohari@gmail.com', [user.email])
        return user
		
		
		
		
class PlaylistCreationForm(forms.ModelForm):
    playlistname = forms.RegexField(label="Playlist Name", max_length=30, regex=r'^[\w.@+-]+$',
                                help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
                                error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
    
    discription = forms.CharField(label="Description", widget=forms.TextInput,
                                help_text = "Enter the same password as above, for verification.")
    
    class Meta:
        model = User
        fields = ("playlistname",)

    def clean_playlistname(self):
        playlistname = self.cleaned_data.get("playlistname", "")
        description = self.cleaned_data["description"]        
    
    def description(self):
        description = self.cleaned_data["description"]
        playlistname1 = playlist.objects.filter(playlistname1__iexact=playlistname1)
        if len(playlistname1) >= 1:
            raise forms.ValidationError("Playlist name already exist.")
        return description

    
    def save(self, commit=True, domain_override=None,
        ##email_template_name='registration/signup_email.html',
        use_https=False, token_generator=default_token_generator):
        playlist = super(PlaylistCreationForm, self).save(commit=False)
        ######NOT SURE############
        #user.first_name = firstname 
        #user.last_name = lastname
        ##########################
        ##user.set_password(self.cleaned_data["password1"])
        ##user.email = self.cleaned_data["email1"]
        playlist.is_active = False
        if commit:
            playlist.save()
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
            
            'domain': domain,
            'site_name': site_name,
            'uid': int_to_base36(plalist.id),
            'user': playlist,
            'token': token_generator.make_token(playlist),
            'protocol': use_https and 'https' or 'http',
            }
        
        return playlist		
		

class SharePlaylistCreationForm(forms.ModelForm):
    playlistname = forms.RegexField(label="Playlist Name", max_length=30, regex=r'^[\w.@+-]+$',
                                help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
                                error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
    
    discription = forms.CharField(label="Description", widget=forms.TextInput,
                                help_text = "Enter the same password as above, for verification.")
    
    class Meta:
        model = User
        fields = ("playlistname",)

    def clean_playlistname(self):
        playlistname = self.cleaned_data.get("playlistname", "")
        description = self.cleaned_data["description"]        
    
    def description(self):
        description = self.cleaned_data["description"]
        playlistname1 = playlist.objects.filter(playlistname1__iexact=playlistname1)
        if len(playlistname1) >= 1:
            raise forms.ValidationError("Playlist name already exist.")
        return description

    
    def share(self, commit=True, domain_override=None,
        ##email_template_name='registration/signup_email.html',
        use_https=False, token_generator=default_token_generator):
        shareplaylist = super(SharePlaylistCreationForm, self).share(commit=False)
        ######NOT SURE############
        #user.first_name = firstname 
        #user.last_name = lastname
        ##########################
        ##user.set_password(self.cleaned_data["password1"])
        ##user.email = self.cleaned_data["email1"]
        shareplaylist.is_active = False
        if commit:
            shareplaylist.share()
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
            
            'domain': domain,
            'site_name': site_name,
            'uid': int_to_base36(plalist.id),
            'user': shareplaylist,
            'token': token_generator.make_token(playlist),
            'protocol': use_https and 'https' or 'http',
            }
        
        return shareplaylist	


class ViewEditPlaylistCreationForm(forms.ModelForm):
    playlistname = forms.RegexField(label="Playlist Name", max_length=30, regex=r'^[\w.@+-]+$',
                                help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
                                error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
    
    discription = forms.CharField(label="Description", widget=forms.TextInput,
                                help_text = "Enter the same password as above, for verification.")
    
    class Meta:
        model = User
        fields = ("playlistname",)

    def clean_playlistname(self):
        playlistname = self.cleaned_data.get("playlistname", "")
        description = self.cleaned_data["description"]        
    
    def description(self):
        description = self.cleaned_data["description"]
        playlistname1 = playlist.objects.filter(playlistname1__iexact=playlistname1)
        if len(playlistname1) >= 1:
            raise forms.ValidationError("Playlist name already exist.")
        return description

    
    def viewedit(self, commit=True, domain_override=None,
        ##email_template_name='registration/signup_email.html',
        use_https=False, token_generator=default_token_generator):
        vieweditplaylist = super(ViewEditPlaylistCreationForm, self).viewedit(commit=False)
        ######NOT SURE############
        #user.first_name = firstname 
        #user.last_name = lastname
        ##########################
        ##user.set_password(self.cleaned_data["password1"])
        ##user.email = self.cleaned_data["email1"]
        vieweditplaylist.is_active = False
        if commit:
            vieweditplaylist.viewedit()
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
            
            'domain': domain,
            'site_name': site_name,
            'uid': int_to_base36(plalist.id),
            'user': vieweditplaylist,
            'token': token_generator.make_token(vieweditplaylist),
            'protocol': use_https and 'https' or 'http',
            }
        
        return vieweditplaylist					