from django.db import models
from django.db.models.signals import post_save

#import usermgr.models
#from django.bd import personallibrary.models

# Create your models here.
# Reflibrary   (Lyon)

class Medium(models.Model):
    name = models.CharField('Medium name', max_length=50)
    description = models.TextField('Medium description', max_length=50)
    
    def __unicode__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField('Artist name', max_length=100)
    homepage = models.URLField()
    bio = models.TextField()
    
    def __unicode__(self):
        return self.name
        
class Role(models.Model):
    name = models.CharField('Role name', max_length=50)
    
    def __unicode__(self):
        return self.name

class RecordCategory(models.Model):
    name = models.CharField('Category name', max_length=100)
    description = models.CharField('Category description', max_length=100)
    number_of_disc = models.IntegerField('Number of discs of each record in this category')
    
    def __unicode__(self):
        return self.name
        
    class Meta(object):
        verbose_name_plural = "Record Categories"
    
class Genre(models.Model):
    name = models.CharField('Genre Name', max_length=50)
    
    def __unicode__(self):
        return self.name

class Style(models.Model):
    name = models.CharField('Style Name', max_length=50)
    
    genre_type = models.ForeignKey(Genre)
    
    def __unicode__(self):
        return self.name
    

class Rhythm(models.Model):
    name = models.CharField('Rhythm Name', max_length=50)
    
    def __unicode__(self):
        return self.name

class SoundTrack(models.Model):
    name = models.CharField('Track Title', max_length=50)
    #artist = models.CharField('Artist Name',max_length=50)
    #trackfile= models.FileField(upload_to=None)
    release_date= models.DateField('Track Release Date')
    duration = models.CharField('Track Duration', max_length=50)
    original_version = models.URLField()
    label = models.CharField('Track Label',max_length=100)  
    
    style_type = models.ForeignKey(Style)
    rhythm_type = models.ForeignKey(Rhythm)
    artists = models.ManyToManyField(Artist, through='SoundTrackFeaturing')
    
    def __unicode__(self):
        return self.name

# the intermediary model between SoundTrack - Artist
# many-to-many relationship.
class SoundTrackFeaturing(models.Model):
    role = models.ForeignKey(Role)
    
    soundtrack = models.ForeignKey(SoundTrack)
    artist = models.ForeignKey(Artist)
    
    def __unicode__(self):
        return self.role.__unicode__()

class Record(models.Model):
    title = models.CharField('Record title', max_length=50)
    matrix_number = models.CharField('Record\'s matrix number', max_length=50)
    cover_art = models.ImageField(upload_to='cover_arts')
    
    category = models.ForeignKey(RecordCategory)
    medium = models.ForeignKey(Medium)
    soundtrack = models.ManyToManyField(SoundTrack)
    artists = models.ManyToManyField(Artist, through='RecordFeaturing')
    
    def __unicode__(self):
        return self.title

# the intermediary model between Record - Artist
# many-to-many relationship.
class RecordFeaturing(models.Model):
    role = models.ForeignKey(Role)
    
    record = models.ForeignKey(Record)
    artist = models.ForeignKey(Artist)
    
    def __unicode__(self):
        return self.role.__unicode__()
