from tkinter.tix import Tree
from django.db import models
from regsiter.models import *

class Cashbacks(models.Model):
    price = models.CharField(max_length=250,null=True,blank=True)
    shops = models.ForeignKey(Shops,on_delete=models.CASCADE,null=True,blank=True)
    client = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True)
    is_cashback = models.BooleanField(default = False)
    date = models.DateTimeField(auto_now_add=True)

class SaveCashback(models.Model):
    cashback = models.FloatField(null=True,blank=True)
    cashbak_id = models.ForeignKey(Cashbacks,on_delete = models.CASCADE,null=True,blank=True)
    