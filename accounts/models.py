from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    
    age = models.IntegerField(default=0)
    
    role_choices = ((0, 'Admin'),
    (1, 'Polling Authority'),)
    
    role = models.IntegerField(choices=role_choices,default=0)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    symbol = models.ImageField(upload_to='party_symbols/')
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - {self.party}"

    
class Voter(models.Model):
    name = models.CharField(max_length=100)
    election_id = models.CharField(max_length=100, unique=True)
    face_encoding = models.TextField() # base64 or numpy array as string
    has_voted = models.BooleanField(default=False)
    def __str__(self):
        return self.name



class Election(models.Model):
    
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            Election.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

  
  
  
  # models.py


#new one
from django.db import models

class ElectionMention(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# python manage.py makemigrations
# python manage.py migrate
