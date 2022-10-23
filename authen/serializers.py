from email.headerregistry import Group
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from regsiter.models import *
from django.contrib.auth.models import User


class AllGroupsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserSiginUpserializers(serializers.ModelSerializer):
    groups = AllGroupsSerializers(read_only=True, many=True)
    class Meta:
        model = CustumUsers
        fields = ['username','password','groups']

class UserLoginSerializers(serializers.ModelSerializer):
    username = serializers.CharField(max_length=250)
    class Meta:
        model = CustumUsers
        fields = ['username','password',]

    

class UserPorfilesSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = ['id','username','first_name','last_name',]