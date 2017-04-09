from django import forms
from .models import Device
from django.contrib.auth.forms import AuthenticationForm 
from django.forms import ModelForm

class DeviceForm(forms.Form):
    
     device = forms.CharField(label="Device", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'Device'}))
     command = forms.ChoiceField(choices=[(x,y)  for x,y in enumerate(["on","off"])])


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class CreateDeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['name','manufacturer_id','device_type','location']
    
