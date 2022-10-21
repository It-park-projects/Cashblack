from enum import unique
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

class MyUserManager(BaseUserManager):

    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError('User must have a valid username')

        user = self.model(phone=phone)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        if not phone:
            raise ValueError('User must have a valid username')

        user = self.model(phone=phone)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustumUsers(AbstractUser):
    phone = models.CharField(max_length=100,null=True,blank=True,unique=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []



class Cataegor(models.Model):
    title = models.CharField(max_length=250)
    logo = models.ImageField(upload_to='logo_categor/',null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title