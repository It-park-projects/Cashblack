from unicodedata import category
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from regsiter.models import *

from regsiter.models import *
from django import forms 

class CreasteUser(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustumUsers
        fields = ('username','first_name','last_name','code_s','password')


class ChangeUser(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustumUsers
        fields = ('username','first_name','last_name','code_s','password')

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

class ShopsPaymentSumm(forms.ModelForm):
    class Meta:
        model = Shops
        fields = ['payment_summ',]
        widgets = {
            'payment_summ': forms.TextInput(attrs={'class':'form-control'}),
        }

        labels = {
            'payment_summ': "To'lov summasi",
        }

