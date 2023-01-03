from django.db import models
from regsiter.models import *


class Blance(models.Model):
    blance = models.CharField(max_length=250,null=True,blank=True)
    user_id = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True)
    shop_id = models.ForeignKey(Shops,on_delete=models.CASCADE,null=True,blank=True)
    payment_date = models.DateField(auto_now=False,auto_now_add=True)

class NotificationStatus(models.Model):
    name = models.CharField(max_length=250,null=True,blank=True)

    def __str__(self):
        return self.name

class NotifikationsSendClient(models.Model):
    title = models.CharField(max_length=250,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    img = models.ImageField(upload_to='notifikation/',null=True,blank=True)
    status_id = models.IntegerField(default=1,null=True,blank=True)
    shop_id = models.ForeignKey(Shops,on_delete=models.CASCADE,null=True,blank=True)
    author_id = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    
