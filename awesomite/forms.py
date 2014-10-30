from django import forms
from awesomite.models import tasks

class todoform(forms.ModelForm):
    title = forms.CharField(max_length=250, help_text="Please enter a title")
    description = forms.CharField(max_length=400, help_text="Please enter title description")
    time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])

    class Meta:
        model = tasks
        fields = ('title','description','time')