from enum import unique
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.files import File
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import random
from authen.servise import send_message

class Cataegor(models.Model):
    title = models.CharField(max_length=250)
    logo = models.ImageField(upload_to='logo_categor/',null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
class Province(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name
class Distric(models.Model):
    name = models.CharField(max_length=250)
    provie_id = models.ForeignKey(Province,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.name
class Shops(models.Model):
    name_shops = models.CharField(max_length=250,null=True,blank=True,unique=True)
    brand_img = models.ImageField(upload_to='brands/',null=True,blank=True)
    cashback = models.IntegerField(null=True,blank=True)
    categor_id = models.ForeignKey(Cataegor,on_delete=models.CASCADE,null=True,blank=True)
    provinse_id = models.ForeignKey(Province,on_delete=models.CASCADE,null=True,blank=True)
    distrik_id = models.ForeignKey(Distric,on_delete=models.CASCADE,null=True,blank=True)
    user_id = models.IntegerField(null=True,blank=True)
    payment_summ = models.CharField(max_length=250,null=True,blank=True)
    is_payment = models.BooleanField(default=False,null=True,blank=True)
    payemnt_date = models.DateField(null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name_shops
class CustumUsers(AbstractUser):
    code_s = models.CharField(max_length=100,null=True,blank=True,unique=True)
    promo_code = models.CharField(max_length=250,null=True,blank=True)
    shops_id = models.ManyToManyField(Shops,blank=True)
    appSignature = models.CharField(max_length=250,null=True,blank=True)
    barcode_id = models.CharField(max_length=200,blank=True)
    barcode=models.ImageField(upload_to='images/',blank=True) 
    def save_product(self,*args,**kwargs):
        EAN=barcode.get_barcode_class('ean13')
        barcode_generator = random.randint(1000000000000, 9999999999999)
        ean=EAN(str(barcode_generator),writer=ImageWriter())
        buffer=BytesIO()
        ean.write(buffer)
        self.barcode_id = ean
        self.barcode.save(f'{self.username}.png',File(buffer),save=False)
        return super().save(*args,**kwargs)
    def send_sms(self,*args,**kwargs,):
        code_s = str(random.randint(10000,99999)) 
        send_message(self.username,code_s)
        return code_s













