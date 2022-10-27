from http import client
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


class ShopsAllSerializers(serializers.ModelSerializer):
    categor_id = AllCategorSerializers(read_only=True)
    provinse_id = AllProviseSerializers(read_only=True)
    distrik_id = AllDistricSerializers(read_only=True)
    user_id = UserPorfilesSerializers(read_only=True)
    class Meta:
        model = Shops
        fields = ['id','name_shops','cashback','categor_id','provinse_id','distrik_id',]

class ShopsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = ['name_shops','brand_img','cashback','categor_id','provinse_id','distrik_id','user_id']
    def create(self, validated_data):
        print(validated_data['name_shops'])
        validated_data['user_id'] = self.context.get('user_id')
        return super(ShopsSerializers,self).create(validated_data)
    def update(self, instance, validated_data):
        instance.name_shops = validated_data.get('name_shops',instance.name_shops)
        instance.brand_img = validated_data.get('brand_img',instance.brand_img)
        instance.cashback = validated_data.get('cashback',instance.cashback)
        instance.categor_id = validated_data.get('categor_id',instance.categor_id)
        instance.provinse_id = validated_data.get('provinse_id',instance.provinse_id)
        instance.distrik_id = validated_data.get('distrik_id',instance.distrik_id)
        # self.context.get('')
        instance.save() 
        return instance

class CustomUserClientsSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = ['id','first_name','last_name','username','password','groups',]
    def create(self,validate_date):
        client_create = CustumUsers.objects.create_user(
            first_name = validate_date['first_name'],
            last_name = validate_date['last_name'],
            username = validate_date['username'],
        )
        client_create.set_password(validate_date['password'])
        for i in validate_date['groups']:
            client_create.groups.add(i.id)
        client_create.save()
        return client_create
    def update(self,instance,validate_data):
        instance.first_name = validate_data.get('first_name',instance.first_name)
        instance.last_name = validate_data.get('last_name',instance.last_name)
        instance.username = validate_data.get('username',instance.username)
        instance.set_password(validate_data.get('password',instance.password))
        instance.groups.set(validate_data.get('groups',instance.groups)) 
        instance.save()
        return instance
class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = '__all__'