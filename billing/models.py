from django.db import models
from regsiter.models import *


class Blance(models.Model):
    blance = models.CharField(max_length=250,null=True,blank=True)
    user_id = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True)
    shop_id = models.ForeignKey(Shops,on_delete=models.CASCADE,null=True,blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    
