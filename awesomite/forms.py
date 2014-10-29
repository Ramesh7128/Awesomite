from django import forms
from awesomite.models import tasks

class todoform(forms.ModelForm):
    title = models.CharField(max_length=250, help_text="Please enter a title")
    description = models.CharField(max_length=400, help_text="Please enter title description")
    priority = models.CharField(max_length=1, choices=PRIORITY)
    time = models.DateTimeField()

    class Meta:
        model = tasks
        fields = ('title','description','priority','time')