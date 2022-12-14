from django.contrib.auth.models import User,Group
from rest_framework import serializers
from rest_framework.serializers import Serializer,ImageField
from regsiter.models import *
from billing.models import *

class ShopsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = '__all__'

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = ['id','username','first_name','last_name',]

class BalanceSerializers(serializers.ModelSerializer):
    shop_id = ShopsSerializers(read_only=True)
    class Meta:
        model = Balans
        fields = ['id','amunt','is_date','date','shop_id',]

class HistoryPamentSerialzers(serializers.ModelSerializer):
    shop_id = ShopsSerializers(read_only=True)
    class Meta:
        model = PaymentHistory
        fields = ['id','amount','card_number','expire_date','shop_id','payment_date',]


class CreateBillingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balans
        fields = '__all__'
    def create(self,validate_date):
        get_number = str(validate_date.get('blance'))
        replace_number = get_number.replace(' ','')
        balance_create  = Balans.objects.create(
            blance = replace_number,
            user_id = self.context.get('user_id'),
            shop_id = self.context.get('shop_id')  
        )
        return balance_create


class NotificationStatusse(serializers.ModelSerializer):
    class Meta:
        model = NotificationStatus
        fields = '__all__'


class AllNotificationSmsSerializers(serializers.ModelSerializer):
    shop_id = ShopsSerializers(read_only=True)
    class Meta:
        model = NotifikationsSendClient
        fields = '__all__'

class CreateNotificationSmsSerializers(serializers.ModelSerializer):
    img = serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = NotifikationsSendClient
        fields =  '__all__'
    def create(self, validated_date):
        notification_create = NotifikationsSendClient.objects.create(**validated_date)
        notification_create.shop_id = self.context.get('shop_id')
        notification_create.user_id = self.context.get("user_id")

        # print(self.context.get("user_id"))
        shop = Shops.objects.get(user_id=self.context.get("users_id"))
        balans = Balans.objects.get(shop_id=shop.id)
        for item in NotificationStatus.objects.all():
            if int(balans.amunt) <= int(item.name):
                raise serializers.ValidationError({"error":"Hisobingizda yetarli mablag' mavjud emas"})
        summ = int(balans.amunt)-int(item.name)
        balans_confirm = Balans.objects.filter(shop_id=shop.id).update(amunt=str(summ))
        notification_create.save()
        return notification_create

    def update(self,instance,validate_data):
        instance.title = validate_data.get('title',instance.title)
        instance.content = validate_data.get('content',instance.content)
        instance.img = validate_data.get('img',instance.img)
        instance.save()
        return instance


class NotificationShopSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = ['id','name_shops','brand_img',]

class AllNotificationClientSerializers(serializers.ModelSerializer):
    shop_id = NotificationShopSerializers(read_only=True)
    class Meta:
        model = NotifikationsSendClient
        fields =  ['title','content','img','shop_id','date',]