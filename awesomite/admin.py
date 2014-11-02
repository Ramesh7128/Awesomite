from django.contrib import admin
from awesomite.models import tasks, Userprofile


admin.site.register(Userprofile)
admin.site.register(tasks)