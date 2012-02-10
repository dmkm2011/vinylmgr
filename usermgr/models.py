from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# The user profile.
# Since Django already has its model for User (from django.contrib.auth),
# we jsut need to extend this model to store the specific information for our app.
# This technique is described at 
# https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users

# We also use 'ImageField' for avatar, so we need the Python Imageging Library.

# More information about Django's built-in models at 
# https://docs.djangoproject.com/en/dev/ref/models/fields

# Also used extra fields on many-to-many relationship.
# This technique is described in:
#https://docs.djangoproject.com/en/dev/topics/db/models/#extra-fields-on-many-to-many-relationships

class PlatformLanguage(models.Model):
    LANGUAGE_NAME_CHOICES=(
	('EN', 'English'),
	('FR', 'French'),
    )
    name = models.CharField(max_length=2, choices=LANGUAGE_NAME_CHOICES,default=LANGUAGE_NAME_CHOICES[0][0])
    
    def __unicode__(self):
        return self.name
	

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # username, password, firstname, lastname, email
    # are already included in Django's User model.
    biography = models.TextField()
    avatar = models.ImageField(upload_to='avatars')
    personal_page = models.URLField()
    published_tracklist = models.BooleanField()
    published_ownedlist = models.BooleanField()
    
    # relationships
    # null = True to deal with the auth package when it create the admin user.
    # should never be null in practice.
    platform_language = models.ForeignKey(PlatformLanguage, null=True)
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance, platform_language = None)

    post_save.connect(create_user_profile, sender=User)
    
    def __unicode__(self):
        return self.user.username
	
#(No need to implement RecordBackup and SoundTrackBackup right now, we will find a way for the backup-and-restore functionality).    
