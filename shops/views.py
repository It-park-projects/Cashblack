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
        serializers = CrudCashbakSerializers(data=request.data,context={'client_id':check_barcode.id, "user_id":request.user.id,'shops':request.user.shops_id.all(),'is_cashback':is_cashback,'check_cashbeck_sell':check_cashbeck_sell})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'Create Sucsess'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)





class StatisticsTodayCashbacks(APIView):
    def get(self,request,format=None):
        all_list_payments = []
        today = date.today()
        add_30_day = today + relativedelta(days=30)

        try:get_Shop = Shops.objects.get(user_id=request.user.id)
        except Shops.DoesNotExist: get_Shop=None
        for i in Cashbacks.objects.filter(shops__id = get_Shop.id,date = today):

            # ,date__day = date.today().day
            all_list_payments.append({
                'phone':i.client.username,
                'price':i.price,
                'cashback':int(i.price) * (get_Shop.cashback / 100),
                'salesman':f'{i.user_id.first_name} {i.user_id.last_name}',
                'date':i.date
            })
        return Response({'list':all_list_payments})

class StatisticsCashbacksFilter(APIView):
    def get(self,request,start_date,end_date,format=None):
        all_list_payments = []
        try:get_Shop = Shops.objects.get(user_id=request.user.id)
        except Shops.DoesNotExist: get_Shop=None
        start_date_get = parse_date(start_date)
        end_date_get = parse_date(end_date) + relativedelta(months=1)
        for k in range(start_date_get.month,end_date_get.month,1):
            for i in Cashbacks.objects.filter(shops__id = get_Shop.id,date__month = k):
                all_list_payments.append({
                    'phone':i.client.username,
                    'price':i.price,
                    'cashback':int(i.price) * (get_Shop.cashback / 100),
                    'salesman':f'{i.user_id.first_name} {i.user_id.last_name}',
                })
        return Response({'list':all_list_payments})

class CashbackStatistics(APIView):
    def get(self,request,start_date,end_date,format=None):
        all_list_payments = []
        csh = 0
        cshprice = 0
        start_date_get = parse_date(start_date)
        end_date_get = parse_date(end_date) + + relativedelta(months=1)
        try:get_Shop = Shops.objects.get(user_id=request.user.id)
        except Shops.DoesNotExist: get_Shop=None
        for k in range(start_date_get.month,end_date_get.month,1):
            for i in Cashbacks.objects.filter(shops__id = get_Shop.id,date__month = k,is_cashback = True,date__year = date.today().year):
                cshprice += (i.price * (get_Shop.cashback / 100))
                csh += i.price
                try: get_cashbacks =  SaveCashback.objects.get(cashbak_id = i.id)
                except SaveCashback.DoesNotExist: get_cashbacks = None
                all_list_payments.append({'phone':i.client.username,'all_payed_cashback':csh,'cashback':cshprice,})
        return Response({'list':all_list_payments})
    
class ClientCategory(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        list_categories = []
        list_cate_all = []
        for i in request.user.shops_id.all():
            list_categories.append({
                'id':i.categor_id.id,
                'name':i.categor_id.title,
                'image':i.categor_id.logo.url
            })
        for k in dict((v['id'],v) for v in list_categories).values():
            list_cate_all.append({
                'id':k['id'],
                'name':k['name'],
                'logo':k['image']
            })
        return Response(list_cate_all,status=status.HTTP_200_OK)

class ClientShops(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,pk,format=None):
        list_shop = []
        for i in request.user.shops_id.all():
            if i.categor_id.id == pk:
                list_shop.append({
                    'id':i.id,
                    'name_shop': i.name_shops,
                    'brand_img':i.brand_img.url
                })
        return Response(list_shop,status=status.HTTP_200_OK)

class ClientShopsStatistics(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,id,format=None):
        x= []
        try: get_shop =  Cashbacks.objects.get(shops__id=id,client = request.user.id)
        except Cashbacks.DoesNotExist: get_shop = None
        x.append({
            'price':get_shop.price,
            'csh_persent':get_shop.shops.cashback,
            'csh':int(get_shop.price) * (get_shop.shops.cashback / 100),
            'date':get_shop.date
        })
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
                x.append({
                    'price':i.price,
                    'csh_persent':i.shops.cashback,
                    'csh':int(i.price) * (i.shops.cashback / 100),
                    'date':i.date
                })
        return Response(x,status=status.HTTP_200_OK)