from django.db import models

# Create your models here.
class tasks(models.Model):

    title = models.CharField(max_length=250)
    description = models.CharField(max_length=400)
    time = models.DateTimeField()

    def __unicode__(self):
        return self.title

