from django.db import models

# Create your models here.
class tasks(models.Model):
    PRIORITY = (('H','High'),('M','Medium'),('L','Least'))
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=400)
    priority = models.CharField(max_length=1, choices=PRIORITY)
    time = models.DateTimeField()

    def __unicode__(self):
        return self.title

