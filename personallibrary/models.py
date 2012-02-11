from django.db import models
from reflibrary.models import *
from usermgr.models import *

class Rating(models.Model):
    RATING_CHOICES=(
	(1, 'one star'),
	(2, 'two stars'),
	(3, 'three stars'),
	(4, 'four stars'),
	(5, 'five stars'),
    )
    rate = models.IntegerField(choices=RATING_CHOICES)
    
    #relationships
    user = models.ForeignKey(UserProfile)
    record = models.ForeignKey(Record)
    
    def __unicode__(self):
        return self.rate

class Comment(models.Model):
    timestamp = models.DateTimeField()
    content = models.TextField()
    
    #relationships
    user = models.ForeignKey(UserProfile)
    record = models.ForeignKey(Record)
    
    def __unicode__(self):
        return self.content

class TrackedRecordList(models.Model):
    tracked_time = models.DateTimeField()
    
    #relationships
    user = models.ForeignKey(UserProfile)
    record = models.ForeignKey(Record)
    
    def __unicode__(self):
        return self.tracked_time.isoformat()


####################################################################

# Mint, EX, VG or G. For an entry which is a vinyl, its condition will be Vinyl.
# See the full condition list at http://www.cdandlp.com/aide/grading.cfm?lng=2

class EntryCondition(models.Model):
    name = models.CharField('Entry condition', max_length=50)
    description = models.CharField(max_length = 200)
    
    def __unicode__(self):
        return self.name


class PersonalEntryAttribute(models.Model):
    name = models.CharField('Costom field name', max_length = 50)
    description = models.CharField('Custom field description', max_length = 100)
    
    user = models.ForeignKey(UserProfile)
    
    def __unicode__(self):
        return name
        
class UserEntry(models.Model):
    record = models.ForeignKey(Record)
    user = models.ForeignKey(UserProfile)
    condition = models.ForeignKey(EntryCondition)
    
    personal_entries = models.ManyToManyField(PersonalEntryAttribute, through='EntryAttributes')
    
    def __unicode__(self):
        return record

# the intermediary model between UserEntry - PersonalEntryAttribute
# many-to-many relationship.
class EntryAttributes(models.Model):
    value = models.CharField('Value of the personal entry', max_length=100)
    entry = models.ForeignKey(UserEntry)
    attribute = models.ForeignKey(PersonalEntryAttribute)
    
    def __unicode__(self):
        return value

class Playlist(models.Model):
    PRIVACY_CHOICES=(
	(0, 'Private'),
	(1, 'Read-only'),
	(2, 'Writable')	
    )
    PUBLISH_CHOICES = (
    (0, 'Unpublished'),
    (1, 'Published')
    )
    name = models.CharField('Playlist name', max_length = 100)
    description = models.CharField('Playlist description', max_length = 200)
    created_time = models.DateTimeField()
    privacy = models.IntegerField(choices=PRIVACY_CHOICES)
    published = models.IntegerField(choices=PUBLISH_CHOICES)

    workers = models.ManyToManyField(UserProfile, through='PlaylistWorker')
    
    def __unicode__(self):
        return name

# the intermediary model between UserProfile - Playlist
# many-to-many relationship.
class PlaylistWorker(models.Model):
    ROLE_CHOICES=(
	(0, 'Owner'),
	(1, 'Co-worker')
    )
    role = models.IntegerField('Role of user in the playlist', choices=ROLE_CHOICES)
    user = models.ForeignKey(UserProfile)
    playlist = models.ForeignKey(Playlist)
    
    def __unicode__(self):
        return role
        
class SoundTrackInPlaylist(models.Model):
    play_order = models.IntegerField('Order of this soundtrack in the playlist')
    soundtrack = models.ForeignKey(SoundTrack)
    user_entry = models.ForeignKey(UserEntry)
    playlist = models.ForeignKey(Playlist)
    
    def __unicode__(self):
        return play_order;
