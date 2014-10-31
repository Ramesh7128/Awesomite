from django import forms
from awesomite.models import tasks

class todoform(forms.ModelForm):
    title = forms.CharField(max_length=250, help_text="Title")
    description = forms.CharField(max_length=400, help_text="Description")
    time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'],help_text="Time")

    class Meta:
        model = tasks
        # widgets = {'date': forms.DateInput(attrs={'id': 'datepicker'})}
        fields = ('title','description','time')