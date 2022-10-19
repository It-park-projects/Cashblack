from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from register.models import *
from django import forms 

class CreasteUser(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustumUsers
        fields = ('username','first_name','last_name','phone','password')


class ChangeUser(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustumUsers
        fields = ('username','first_name','last_name','phone','password')
