from django.db import models
from regsiter.models import *


class PaymentHistory(models.Model):
    amount = models.CharField(max_length=250,null=True,blank=True)
    card_number = models.CharField(max_length=250,null=True,blank=True)
    expire_date = models.CharField(max_length=100,null=True,blank=True)
    extra_id = models.CharField(max_length=250,null=True,blank=True)
    user_id = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True)
    shop_id = models.ForeignKey(Shops,on_delete=models.CASCADE,null=True,blank=True)
    payment_date = models.DateTimeField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return self.card_number

class Balans(models.Model):
    amunt = models.CharField(max_length=250,null=True,blank=True,default='0')
    shop_id = models.ForeignKey(Shops,on_delete=models.CASCADE,null=True,blank=True)
    payment_id = models.ForeignKey(PaymentHistory,on_delete=models.CASCADE,null=True,blank=True)
    is_date = models.BooleanField(default=False,null=True,blank=True)
    last_date = models.DateTimeField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

   


class NotificationStatus(models.Model):
    name = models.CharField(max_length=250,null=True,blank=True,default='0')

    def __str__(self):
        return self.name

class NotifikationsSendClient(models.Model):
    title = models.CharField(max_length=250,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    def nameFile(instance,filename):
        return '/'.join(['notifikation', str(instance.title), filename])
    img = models.ImageField(upload_to=nameFile,null=True,blank=True)
    status_id = models.IntegerField(default=1,null=True,blank=True)
    payment_summ = models.ForeignKey(NotificationStatus,on_delete=models.CASCADE,null=True,blank=True)
    shop_id = models.ForeignKey(Shops,on_delete=models.CASCADE,null=True,blank=True)
    user_id = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    
