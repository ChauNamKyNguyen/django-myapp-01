from django.db import models

# Utility package
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Actress(models.Model):
    name = models.CharField(max_length=128, unique=True)
    view = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    image = models.ImageField(upload_to='actress_images/', blank=True)
    slug = models.SlugField()
    
    def save(self, *args, **kwargs):
        if (self.view < 0):
            self.view = 0
            
        if (self.like < 0):
            self.like = 0
            
        self.slug = slugify(self.name)
        super(Actress, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Movie(models.Model):
    actress = models.ForeignKey(Actress, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    date = models.DateTimeField('Update date', blank=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # Links USerProfile to a User model
    # Use one-one relationship so that other models who need to use User model 
    # can share the same data
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Additional attributes 
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images/', blank=True)
    
    def __str__ (self):
        return self.user.username

        
        