from django.db import models
from django.contrib import auth
from django.utils import timezone

# Create your models here.

class User(auth.models.User, auth.models.PermissionsMixin):
    
    def __str__(self):
        return self.username


class ContactUser(models.Model):
    name = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=100)
    subject =  models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name