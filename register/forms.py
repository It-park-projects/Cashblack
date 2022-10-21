from unicodedata import category
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from register.models import *

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

class CreateCatgeorForms(forms.ModelForm):
    class Meta:
        model = Cataegor
        fields = '__all__'
    
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'logo': forms.FileInput(attrs={'class':'form-control'}),
        }

        labels = {
            'title': "Kategoriya nomi",
            'logo':'Logotib kategoriya',
        }
