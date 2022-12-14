from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from regsiter.models import *
from django.contrib.auth.models import User
from shops.models import Cashbacks, SaveCashback
from billing.models import *
import  datetime

class AllUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = ['id','username','first_name','last_name',]

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
        fields = ['id','name_shops','brand_img','cashback','categor_id','provinse_id','distrik_id','user_id',]

class ShopsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = ['id','name_shops','brand_img','cashback','categor_id','provinse_id','distrik_id','user_id',]
    def create(self, validated_data):
        create_shop = Shops.objects.create(**validated_data)
        create_shop.user_id = self.context.get('user_id')
        create_shop.save()
        try:
            user_get = CustumUsers.objects.get(id = self.context.get('user_id'))
        except CustumUsers.DoesNotExist:
            user_get = None
        
        user_get.shops_id.add(create_shop.id)
        user_get.save()
        shop = Shops.objects.filter(user_id=self.context.get("user_id")).last()
        blanse = Balans(shop_id=shop,last_date=datetime.datetime.today())
        blanse.save()
        return create_shop
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
    price = serializers.CharField(max_length=250)
    class Meta:
        model = Cashbacks
        fields = ['id','price','shops','client','date']
    def create(self, validated_data):
            get_user = self.context.get('user_id')
            get_Shop = self.context['get_Shop']
            get_number = str(validated_data['price'])
            get_cashbacks = self.context.get('check_cashbeck_sell')
            replace_number = get_number.replace(' ','')
            cashback_divide = int(replace_number) * (get_Shop.cashback/100)
            create_client_sell = Cashbacks.objects.create(price = replace_number,shops = get_Shop, client_id = self.context.get('client_id'))
            create_client_sell.user_id_id = self.context['user_id']
            create_client_sell.is_cashback = self.context.get('is_cashback')
            create_client_sell.save()
            get_update_client_shop = CustumUsers.objects.filter(id = self.context['client_id'])[0]
            for q in self.context['shops']:
                get_update_client_shop.shops_id.add(q)
                get_update_client_shop.save()
            if self.context.get('is_cashback') == "False":
                if SaveCashback.objects.filter(cashbak_id = get_cashbacks).first() == None:
                    save_cashback = SaveCashback.objects.create(cashback = cashback_divide,cashbak_id = create_client_sell)
                else:
                    try:cashback = SaveCashback.objects.get(cashbak_id = get_cashbacks)
                    except SaveCashback.DoesNotExist:cashback = None
                    save_cashback = SaveCashback.objects.filter(cashbak_id = get_cashbacks).update(cashback = cashback.cashback + cashback_divide)
            else:
                try:cashback = SaveCashback.objects.get(cashbak_id = get_cashbacks)
                except SaveCashback.DoesNotExist:cashback = None
                save_cashback = SaveCashback.objects.filter(cashbak_id = get_cashbacks).update(cashback = (cashback.cashback - float(replace_number)) + cashback_divide)
            return create_client_sell
    
class ClientCashbekSerializers(serializers.ModelSerializer):

    shops = ShopsAllSerializers(read_only=True)
    class Meta:
        model = Cashbacks
        fields = ['id','price','shops','date',]


    client = AllUserSerializers(read_only=True)
    class Meta:
        model = Cashbacks
        fields = '__all__'

class ClientCashbackTwoSerializers(serializers.ModelSerializer):
    cashbak_id = ClientCashbekSerializers(read_only=True)
    class Meta:
        model = SaveCashback
        fields = '__all__'


class ClientStatistkSerializers(serializers.ModelSerializer):
    shops_id = ShopsAllSerializers(read_only=True,many=True)
    class Meta:
        model = CustumUsers
        fields = ['id','shops_id']


class CategorSe(serializers.ModelSerializer):
    class Meta:
        model = Cataegor
        fields = '__all__'
class ShopsSer(serializers.ModelSerializer):
    categor_id = CategorSe(read_only=True)
    class Meta:
        model = Shops
        fields = ['id','name_shops','brand_img','categor_id',]

class ClinetCategorSerializers(serializers.ModelSerializer):
    shops = ShopsSer(read_only=True)
    class Meta:
        model = Cashbacks
        fields = ['id','shops',]