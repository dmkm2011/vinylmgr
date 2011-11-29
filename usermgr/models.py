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
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)
    