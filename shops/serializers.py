from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from authen.serializers import UserPorfilesSerializers
from regsiter.models import *
from django.contrib.auth.models import User


class AllCategorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cataegor
        fields = '__all__'

class AllProviseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'

class AllDistricSerializers(serializers.ModelSerializer):
    provice = AllProviseSerializers(read_only=True)
    class Meta:
        model = Distric
        fields ='__all__'


class ShopsSerializers(serializers.ModelSerializer):
    categor_id = AllCategorSerializers(read_only=True)
    provinse_id = AllProviseSerializers(read_only=True)
    distrik_id = AllDistricSerializers(read_only=True)
    auth = UserPorfilesSerializers(read_only=True)
    class Meta:
        model = Shops
        fields = ['id','name','cash_bak','brands','categor_id','provinse_id','distrik_id','auth',]
    def create(self, validated_data):
        return Shops.objects.create(**validated_data)