from django.db import models
#from django.contrib.auth.models import User
from django.db.models.signals import post_save

#import usermgr.models
#from django.bd import personallibrary.models

# Create your models here.
# Reflibrary   (Lyon)

class Medium(models.Model):
	Medium_Name = models.CharField(max_length=50)
	Medium_Description = models.TextField(max_length=50)
	#Medium_ID = models.unique


class Artist(models.Model):
	Artist_Name = models.CharField(max_length=50)
	Artist_Homepage = models.CharField(max_length=50)
	Artist_Bio = models.CharField(max_length=50)	
	
class Role(models.Model):
	Role_Name = models.CharField(max_length=50)
	#Role_ID = models.unique	

class Record_Category(models.Model):
	Category_Name = models.CharField(max_length=50)
	Category_Description = models.CharField(max_length=50)
	Category_NumberOfDisc = models.IntegerField()
	#Category_ID = models.unique
	
class Genre(models.Model):
    name = models.CharField('Genre Name',max_length=50)	

class Style(models.Model):
    name = models.CharField('Style Name',max_length=50)
    genretype = models.ForeignKey('Genre')

class Rythm(models.Model):
    name = models.CharField('Rythm Name',max_length=50)
    
class SoundTrack(models.Model):
    name = models.CharField('Track Title',max_length=50)
    artist= models.CharField('Artist Name',max_length=50)
    #trackfile= models.FileField(upload_to=None)
    release_Date= models.DateField('Track Release Date')
    duration = models.DateTimeField('Track Duration')
    originalversion=models.URLField()
    lable= models.CharField('Track Lable',max_length=50)  
    styleType = models.ForeignKey('Style')
    rythnType = models.ForeignKey('Rythm')


	
class SoundTrackFeaturing(models.Model):
	role = models.ForeignKey(Role)
	soundtrack = models.ForeignKey(Record_Category)
	artist = models.ForeignKey(Artist)
	#SountTrackFeaturing_ID = models.unique
	


class Record(models.Model):
	R_Title = models.CharField(max_length=50)
	R_MatrixNumber = models.IntegerField()
	R_CoverArt = models.CharField(max_length=50)
	record_category = models.ForeignKey(Record_Category)
	medium = models.ForeignKey(Medium)
	soundtrack = models.ManyToManyField(SoundTrack)
	#Medium_ID = models.unique
 
class RecordFeaturing(models.Model):
	record = models.ForeignKey(Record)
	role = models.ForeignKey(Role)
	artist = models.ForeignKey(Artist)
	#RecordFeaturing_ID = models.unique
