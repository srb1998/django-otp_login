from django.db import models
from django.contrib.auth.models import User

# Create your models here.
 
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = None
    mobile = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
