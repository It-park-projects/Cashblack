from tkinter.tix import Tree
from django.db import models
from regsiter.models import *

class Cashbacks(models.Model):
    price = models.CharField(max_length=250,null=True,blank=True)
    shops = models.ForeignKey(Shops,on_delete=models.CASCADE,null=True,blank=True)
    client = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True)
    cashbak = models.IntegerField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.price
