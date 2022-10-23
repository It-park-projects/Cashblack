from enum import unique
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager


class CustumUsers(AbstractUser):
    code_s = models.CharField(max_length=100,null=True,blank=True,unique=True)

  



class Cataegor(models.Model):
    title = models.CharField(max_length=250)
    logo = models.ImageField(upload_to='logo_categor/',null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Province(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.name

class Distric(models.Model):
    name = models.CharField(max_length=250)
    provie_id = models.ForeignKey(Province,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name


class Shops(models.Model):
    name = models.CharField(max_length=250,null=True,blank=True)
    cash_bak = models.IntegerField(null=True,blank=True)
    brands = models.ImageField(upload_to='brands/',null=True,blank=True)
    categor_id = models.ForeignKey(Cataegor,on_delete=models.CASCADE,null=True,blank=True)
    provinse_id = models.ForeignKey(Province,on_delete=models.CASCADE,null=True,blank=True)
    distrik_id = models.ForeignKey(Distric,on_delete=models.CASCADE,null=True,blank=True)
    auth = models.ForeignKey(CustumUsers,on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name