from lib2to3.pytree import type_repr
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from authen.renderers import UserRenderers
from authen.serializers import *
from regsiter.models import *
from shops.serializers import *
from django.shortcuts import get_object_or_404


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
            serializers.save()
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
        serializers = ShopsSerializers(instance=Shops.objects.filter(id=pk)[0],data=request.user.id,partial=True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':"success update"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)

class ClientSellView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def post(self,request,barcode_id,is_cashback,format=None):
        check_barcode = get_object_or_404(CustumUsers,barcode_id = barcode_id)
        check_cashbeck_sell = Cashbacks.objects.filter(client = check_barcode).first()
        serializers = CrudCashbakSerializers(data=request.data,context={'client_id':check_barcode, "user_id":request.user.id,'is_cashback':is_cashback,'check_cashbeck_sell':check_cashbeck_sell})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'Create Sucsess'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)




class StatistikShopsViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,pk,format=None):
        shop = Shops.objects.get(user_id=request.user)
        print(shop)
        cashbak = Cashbacks.objects.filter()
        serializers = ShopsSerializers(shop,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class ClientStatistikaView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        cashbak = Cashbacks.objects.filter(client=request.user.id)
        serializers = ClientCashbekSerializers(cashbak,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK) 
    def get(self,request,format=None):
        shop = Shops.objects.get(user_id=request.user.id)
        cashback = Cashbacks.objects.get(shops=shop.id)
        cash = SaveCashback.objects.filter(cashbak_id=cashback.id)
        serializers = ClientCashbackTwoSerializers(cash,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
