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
    provie_id = AllProviseSerializers(read_only=True)
    class Meta:
        model = Distric
        fields =['id','name','provie_id']


class ShopsSerializers(serializers.ModelSerializer):
    categor_id = AllCategorSerializers(read_only=True)
    provinse_id = AllProviseSerializers(read_only=True)
    distrik_id = AllDistricSerializers(read_only=True)
    user_id = UserPorfilesSerializers(read_only=True)
    class Meta:
        model = Shops
        fields = ['id','name_shops','brand_img','cashback','categor_id','provinse_id','distrik_id','user_id',]
    def create(self, validated_data):
        return Shops.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.name_shops = validated_data.get('name_shops',instance.name_shops)
        instance.brand_img = validated_data.get('brand_img',instance.brand_img)
        instance.cashback = validated_data.get('cashback',instance.cashback)
        instance.categor_id = validated_data.get('categor_id',instance.categor_id)
        instance.provinse_id = validated_data.get('provinse_id',instance.provinse_id)
        instance.distrik_id = validated_data.get('distrik_id',instance.distrik_id)
        instance.save() 
        return instance
    