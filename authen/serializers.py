from django.contrib.auth.models import User,Group
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from regsiter.models import *
from django.contrib.auth.models import User
from shops.serializers import *


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
    groups = AllGroupsSerializers(read_only = True,many=True)
    shops_id = ShopsAllSerializers(read_only = True,many=True)
    class Meta:
        model = CustumUsers
        fields = ['id','username','first_name','last_name','groups','shops_id',]


class UpdateFullNameSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = ['id','first_name','last_name']



class UserUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = '__all__'
    def create(self,validate_date):
        client_create = CustumUsers.objects.create_user(
            first_name = validate_date['first_name'],
            last_name = validate_date['last_name'],
            username = validate_date['username'],
        )
        client_create.set_password(validate_date['password'])
        client_create.shops_id.add(self.context.get('user_id'))
        for i in validate_date['groups']:
            client_create.groups.add(i.id)
        client_create.save_product()
        return client_create
    def update(self,instance,validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.username = validated_data.get('username',instance.username)
        instance.set_password(validated_data.get('password',instance.password))
        # for i in self.context.get('user_id').all():
        #     instance.shops_id.add(i)
            # instance.save()
        # instance.shops_id.set(self.context.get('user_id'))
        instance.code_s = validated_data.get('code_s',instance.code_s)
        instance.save()

        return instance

class UserPhoneUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = ['username','password','code_s',]

    def update(self,instance,validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.set_password(validated_data.get('password',instance.password))
        instance.code_s = validated_data.get('code_s',instance.code_s)

        instance.save()
        return instance


class ClientUserUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = '__all__'
    def update(self,instance,validate_data):
        for i in self.context.get('shops_id').all():
            instance.shops_id.add(i)
        instance.save()
        return instance

class ShopsClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = ['id','username','first_name','last_name',]