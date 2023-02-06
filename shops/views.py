from rest_framework.response import Response
from django.shortcuts import render,redirect

from rest_framework import permissions, status
from rest_framework.decorators import api_view, schema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from authen.renderers import UserRenderers
from authen.serializers import *
from regsiter.models import *
from shops.serializers import *
from django.shortcuts import get_object_or_404
from datetime import date,timedelta
from dateutil.relativedelta import relativedelta
from django.utils.dateparse import parse_date
from datetime import date



class AllCategorViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        categor = Cataegor.objects.all()
        serializers = AllCategorSerializers(categor,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
class AllProvinceViews(APIView):
    def get(self, request, *args, **kwargs):
        categor = Province.objects.all()
        serializers = AllProviseSerializers(categor,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
class AllDistricViews(APIView):
    def get(self, request, *args, **kwargs):
        categor = Distric.objects.all()
        serializers = AllDistricSerializers(categor,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)


class UserShops(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        shops = Shops.objects.filter(user_id=request.user.id)
        serializers = ShopsAllSerializers(shops,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK) 
    def post(self,request,format=None):
        serializers = ShopsSerializers(data=request.data,context={'user_id':request.user.id})
        if serializers.is_valid(raise_exception=True):
            serializers.save(brand_img = request.data.get('brand_img'))
            return Response({'msg':'Create Sucsess'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
class ShopsUpdateViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,pk,format=None):
        shop = Shops.objects.filter(id=pk)
        serializers = ShopsSerializers(shop,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):
        data = request.data
        serializers = ShopsSerializers(instance=Shops.objects.filter(id=pk)[0],data=data,partial=True)
        if serializers.is_valid(raise_exception=True):
            serializers.save(brand_img = request.data.get('brand_img'))
            return Response({'message':"success update"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)



        

class ClientSellView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def post(self,request,barcode_id,is_cashback,format=None):
        check_barcode = get_object_or_404(CustumUsers,barcode_id = barcode_id)
        check_cashbeck_sell = Cashbacks.objects.filter(client = check_barcode).first()
        for i in request.user.shops_id.all():
            get_Shop = Shops.objects.filter(id =i.id)[0]
        print(get_Shop.cashback)
        serializers = CrudCashbakSerializers(data=request.data,context={'client_id':check_barcode.id, "user_id":request.user.id,'shops':request.user.shops_id.all(),'is_cashback':is_cashback,'check_cashbeck_sell':check_cashbeck_sell,'us':request.user,'get_Shop':get_Shop})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'Create Sucsess'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class StatisticsTodayCashbacks(APIView):
    def get(self,request,format=None):
        all_list_payments = []
        delta = (date.today() + relativedelta(days=31)) - date.today()
        get_Shop = Shops.objects.filter(user_id=request.user.id)[0]
        for k in range(delta.days + 1):
            days = date.today() + timedelta(days=k)
            get_cashback_stores = Cashbacks.objects.filter(shops__id = get_Shop.id,date = days)
            for i in get_cashback_stores:
                all_list_payments.append({'phone': i.client.username,'price':i.price,'cashback':int(i.price) * (get_Shop.cashback / 100),'salesman':f'{i.user_id.first_name} {i.user_id.last_name}','date':i.date})
        return Response({'list':all_list_payments})

class StatisticsCashbacksFilter(APIView):
    def get(self,request,start_date,end_date,format=None):
        all_list_payments = []
        get_Shop = Shops.objects.filter(user_id=request.user.id)[0]
        delta = parse_date(end_date) - parse_date(start_date)
        for l in range(delta.days+1):
            days = parse_date(start_date) + timedelta(days=l)
            for i in Cashbacks.objects.filter(shops__id=get_Shop.id, date = days):
                all_list_payments.append({'phone':i.client.username,'price':i.price,'cashback':int(i.price) * (get_Shop.cashback / 100),'salesman':f'{i.user_id.first_name} {i.user_id.last_name}',})
        return Response({'list':all_list_payments})

class ClientCategory(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        list_categories = []
        list_cate_all = []
        for i in request.user.shops_id.all():
            list_categories.append({'id':i.categor_id.id,'name':i.categor_id.title,'image':i.categor_id.logo.url})
        for k in dict((v['id'],v) for v in list_categories).values():
            list_cate_all.append({'id':k['id'],'name':k['name'],'logo':k['image']})
        return Response(list_cate_all,status=status.HTTP_200_OK)

class ClientShops(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,pk,format=None):
        list_shop = []
        for i in request.user.shops_id.all():
            if i.categor_id.id == pk:
                list_shop.append({'id':i.id,'name_shop': i.name_shops,'brand_img':i.brand_img.url})
        return Response(list_shop,status=status.HTTP_200_OK)

class ClientShopsStatistics(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,id,format=None):
        x= []
        try: get_shop =  Cashbacks.objects.get(shops__id=id,client = request.user.id)
        except Cashbacks.DoesNotExist: get_shop = None
        x.append({'price':get_shop.price,'csh_persent':get_shop.shops.cashback,'csh':int(get_shop.price) * (get_shop.shops.cashback / 100),'date':get_shop.date})
        return Response(x,status=status.HTTP_200_OK)
    
class ClientShopStatisticsGet(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,id,start_date,end_date,format=None):
        x = []
        start_date_get = parse_date(start_date)
        end_date_get = parse_date(end_date) + relativedelta(months=1)
        for k in range(start_date_get.month,end_date_get.month,1):
            for i in Cashbacks.objects.filter(shops__id=id,client = request.user.id,date__month = k):
                x.append({'price':i.price,'csh_persent':i.shops.cashback,'csh':int(i.price) * (i.shops.cashback / 100),'date':i.date})
        return Response(x,status=status.HTTP_200_OK)


class StatistikaSumma(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,pk,format=None):
        get_Shop = Shops.objects.filter(user_id=request.user.id)[0]
        delta = (date.today() + relativedelta(days=31)) - date.today()
        sum_price = 0
        sum_cashback = 0
        sum_close_cashback = 0
        list_sts_client = []
        for i in Cashbacks.objects.filter(client = pk):
            sum_price += int(i.price)
            sum_cashback += int(i.price) * (get_Shop.cashback / 100)
            list_sts_client.append({
                'name':i.client.first_name+ " " + i.client.last_name,
                'price':int(i.price),
                'sum_price':sum_price,
                'cashback': int(i.price) * (get_Shop.cashback / 100),
                'sum_cashback':sum_cashback
            })
            if i.is_cashback == True:
                sum_close_cashback += int(i.price) * (get_Shop.cashback / 100)
            separete_cashaback = sum_cashback - sum_close_cashback
        return Response({'client':list_sts_client,'sum_price':sum_price,'sum_cashback':sum_cashback,'sum_close_cashback':sum_close_cashback,'separete_cashaback':separete_cashaback})