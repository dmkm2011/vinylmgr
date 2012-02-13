from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36
from django.template import Context, loader
from django import forms
from reflibrary.models import Record, Artist, SoundTrack

class RecordCreationForm(forms.ModelForm):
    class Meta:
        model = Record

class ArtistCreationForm(forms.ModelForm):
    class Meta:
        model = Artist
        
class SoundTrackCreationForm(forms.ModelForm):
    class Meta:
        model = SoundTrack