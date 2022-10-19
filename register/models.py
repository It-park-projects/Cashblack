from enum import unique
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