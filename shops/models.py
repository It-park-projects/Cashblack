
from django.db import models
from regsiter.models import *
from datetime import date

class Cashbacks(models.Model):
    price = models.CharField(max_length=250,null=True,blank=True)
    shops = models.ForeignKey(Shops,on_delete=models.CASCADE,null=True,blank=True)
    client = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True,related_name='client')
    user_id = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True)
    is_cashback = models.BooleanField(default = False)
    date = models.DateField(auto_now_add=True)

class SaveCashback(models.Model):
    cashback = models.FloatField(null=True,blank=True)
    cashbak_id = models.ForeignKey(Cashbacks,on_delete = models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    