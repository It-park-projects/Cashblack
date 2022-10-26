from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from regsiter.models import *
from django.contrib.auth.models import User
from shops.models import Cashbacks

class AllUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = '__all__'

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
    class Meta:
        model = Shops
        fields = ['id','name_shops','cashback','categor_id','provinse_id','distrik_id','user_id',]

class ShopsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = ['name_shops','brand_img','cashback','categor_id','provinse_id','distrik_id','user_id']
    def create(self, validated_data):
        validated_data['user_id'] = self.context.get('user_id')
        return super(ShopsSerializers,self).create(validated_data)
    def update(self, instance, validated_data):
        instance.name_shops = validated_data.get('name_shops',instance.name_shops)
        instance.brand_img = validated_data.get('brand_img',instance.brand_img)
        instance.cashback = validated_data.get('cashback',instance.cashback)
        instance.categor_id = validated_data.get('categor_id',instance.categor_id)
        instance.provinse_id = validated_data.get('provinse_id',instance.provinse_id)
        instance.distrik_id = validated_data.get('distrik_id',instance.distrik_id)
        instance.save() 
        return instance


class AllCashbakSerializers(serializers.ModelSerializer):
    shops = ShopsAllSerializers(read_only=True)
    client = AllUserSerializers(read_only=True)
    class Meta:
        model = Cashbacks
        fields = ['id','price','shops','client','cashbak','date']

class CrudCashbakSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Cashbacks
        fields = ['id','price','shops','client','cashbak','date']
    def create(self, validated_data):
        get_user = self.context.get('user_id')
        # split_price = validated_data['price'].split(' ','')
        # try:
        get_shop_cashback = Shops.objects.get(user_id = get_user)
        # except Shops.DoesNotExist():
        #     get_shop_cashback = None
        cashback_divide = int(validated_data['price']) * (get_shop_cashback.cashback/100)
        create_client_sell = Cashbacks.objects.create(
            price = validated_data['price'],
            cashbak = cashback_divide,
            shops = get_shop_cashback,
            client = self.context.get('user_id')
        )
        create_client_sell.save()
        # return create_client_sell
        return validated_data['price'] 
