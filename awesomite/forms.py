from django import forms
from django.contrib.auth.models import User
from awesomite.models import tasks, Userprofile
from bootstrap3_datetime.widgets import DateTimePicker

class todoform(forms.ModelForm):
    title = forms.CharField(max_length=250)
    description = forms.CharField(max_length=400)
    time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm","pickSeconds": False}))

    class Meta:
        model = tasks
        # widgets = {'date': forms.DateInput(attrs={'id': 'datepicker'})}
        fields = ('title','description','time')


class Userform(forms.ModelForm):
    password =forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class Userprofileform(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ('phonenumber',)

