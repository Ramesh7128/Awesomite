from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField(User)
    phonenumber = models.IntegerField(max_length=10)

    def __unicode__(self):
        return self.user.username

class tasks(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=400)
    time = models.DateTimeField()

    def __unicode__(self):
        return self.title

