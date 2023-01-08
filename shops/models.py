
from django.db import models
from regsiter.models import *
from datetime import date

class Cashbacks(models.Model):
    price = models.IntegerField(null=True,blank=True)
    shops = models.ForeignKey(Shops,on_delete=models.CASCADE,null=True,blank=True)
    client = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True,related_name='client')
    user_id = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True,related_name='user_id')
    is_cashback = models.BooleanField(default = False)
    date = models.DateTimeField(auto_now_add=True)

class SaveCashback(models.Model):
    cashback = models.FloatField(null=True,blank=True)
    cashbak_id = models.ForeignKey(Cashbacks,on_delete = models.CASCADE,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    