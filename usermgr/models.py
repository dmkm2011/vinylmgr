from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from reflibrary.models import *

# The user profile.
# Since Django already has its model for User (from django.contrib.auth),
# we jsut need to extend this model to store the specific information for our app.
# This technique is described at 
# https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
# We also use 'ImageField' for avatar, so we need the Python Imageging Library.
# More information about Django's built-in models at 
# https://docs.djangoproject.com/en/dev/ref/models/fields

class PlatformLanguage(models.Model):
    LANGUAGE_NAME_CHOICES=(
	('EN', 'English'),
	('FR', 'French'),
    )
    Language_Name=models.CharField(max_length=2, choices=LANGUAGE_NAME_CHOICES)
	

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # username, password, firstname, lastname, email
    # are already included in Django's User model.
    biography = models.TextField()
    avatar = models.ImageField(upload_to='define/a/path/to/store/avatars')
    personal_page = models.URLField()
    published_tracklist = models.BooleanField()
    published_ownedlist = models.BooleanField()
    
    # relationships
    platformlanguage=models.ForeignKey(PlatformLanguage)
	
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)
	
#BELOW TABLES SHOULD BE IN "PERSONAL LIBRARY"
class Rating(models.Model):
    RATING_CHOICES=(
	('1', 'one star'),
	('2', 'two stars'),
	('3', 'three stars'),
	('4', 'four stars'),
	('5', 'five stars'),
    )
    Rate=models.CharField(max_length=1, choices=RATING_CHOICES)
    #relationships
    user=models.ForeignKey(UserProfile)
    record=models.ForeignKey(Record)

class Comment(models.Model):
    Timestamp=models.DateTimeField()
    Content=models.TextField()
    #relationships
    user=models.ForeignKey(UserProfile)
    record=models.ForeignKey(Record)

class TrackedRecordList(models.Model):
    TrackedTime=models.DateTimeField()
    #relationships
    user=models.ForeignKey(UserProfile)
    record=models.ForeignKey(Record)
	
#(No need to implement RecordBackup and SoundTrackBackup right now, we will find a way for the backup-and-restore functionality).    
