from django.db import models
from regsiter.models import *


class Blance(models.Model):
    amount = models.CharField(max_length=250,null=True,blank=True)
    card_number = models.CharField(max_length=250,null=True,blank=True)
    expire_date = models.CharField(max_length=100,null=True,blank=True)
    extra_id = models.CharField(max_length=250,null=True,blank=True)
    user_id = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True)
    shop_id = models.ForeignKey(Shops,on_delete=models.CASCADE,null=True,blank=True)
    payment_date = models.DateTimeField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return self.card_number

class NotificationStatus(models.Model):
    name = models.CharField(max_length=250,null=True,blank=True)

    def __str__(self):
        return self.name

class NotifikationsSendClient(models.Model):
    title = models.CharField(max_length=250,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    def nameFile(instance,filename):
        return '/'.join(['notifikation', str(instance.title), filename])
    img = models.ImageField(upload_to=nameFile,null=True,blank=True)
    status_id = models.IntegerField(default=1,null=True,blank=True)
    shop_id = models.ForeignKey(Shops,on_delete=models.CASCADE,null=True,blank=True)
    author_id = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    
