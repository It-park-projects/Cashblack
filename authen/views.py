import requests
import random
from rest_framework.response import Response
from django.contrib.auth import authenticate,logout
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from authen.renderers import UserRenderers
from authen.serializers import *
from authen.servise import send_message
from regsiter.models import *


# token Olish
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'accsess':str(refresh.access_token)
    }

class AllGroupsViews(APIView):
    render_classes = [UserRenderers]
    def get(self, request, *args, **kwargs):
        gorups = Group.objects.all()
        serializers = AllGroupsSerializers(gorups,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
         
class UserSiginUpViews(APIView):
    render_classes = [UserRenderers]
    def get(self,request,format=None):
        groups = Group.objects.all()    
        serializers = AllGroupsSerializers(groups,many=True)
        return Response(serializers.data,status=status.HTTP_201_CREATED)
    def post(self,request,appSignature):
        username = request.data['username']
        password= request.data['password']
        promo_code = request.data['promo_code']
        if username == "":
            context = {"Tel Raqam Kiritilmadi"}
            return Response(context,status=status.HTTP_401_UNAUTHORIZED)
        us = CustumUsers.objects.filter(username=username)
        if len(us)!=0:
            return Response({'error':"Bunday foydalanuvchi mavjud"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)      
        my_user = CustumUsers.objects.create(username=username,appSignature=appSignature,promo_code=promo_code)
        my_user.set_password(password)
        my_user.save_product()
        toke =get_token_for_user(my_user)
        gr = Group.objects.get(name= 'Biznes')
        my_user.groups.add(gr)  
        return Response({'msg':toke},status=status.HTTP_200_OK)
    def put(self,request,appSignature):
        us = CustumUsers.objects.filter(id=request.user.id)[0]
        code_s = str(random.randint(10000,99999))
        us.code_s=code_s
        us.appSignature=appSignature
        us.save()
        send_message(us.username,us.code_s,us.appSignature)
        return Response({'message':'Sms yubordildi'})

class CreateSotrutnikView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def post(self,request,format=None):
        username = request.data['username']
        password = request.data['password']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        if username=='' or first_name=='' or last_name=='':
            return Response({'error':"Ma'lumotlarni to'ldiring"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        us = CustumUsers.objects.filter(username=username)
        if len(us)!=0:
            return Response({'error':"Bunday foydalanuvchi mavjud"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        s = Shops.objects.filter(user_id=request.user.id)[0]
        my_user = CustumUsers.objects.create(username=username,first_name=first_name,last_name=last_name,)
        my_user.set_password(password)
        my_user.save_product()
        my_user.shops_id.add(s)
        my_user.save()
        gr = Group.objects.get(name= 'Sotrutnik')
        my_user.groups.add(gr)      
        return Response({'msg':"Create Sotrutnik"},status=status.HTTP_200_OK)

class DeleteSotrutnik(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def delete(self,request,pk):
        user = CustumUsers.objects.get(id=pk)
        user.delete()
        return Response({'msg': "Delete Sotrutnik"})

        
class CreateClientView(APIView):
    render_classes = [UserRenderers]    
    perrmisson_class = [IsAuthenticated]
    def post(self,request,appSignature):
        username = request.data['username']
  
        password = request.data['password']
        if username == '':
            return Response({'error':"Ma'lumotlarni to'ldiring"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        us = CustumUsers.objects.filter(username=username)
        if len(us)!=0:
            return Response({'error':"Bunday foydalanuvchi mavjud"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        my_user = CustumUsers.objects.create(username=username,appSignature=appSignature)
        my_user.set_password(password)
        my_user.save_product()
        gr = Group.objects.get(name= 'Client')
        my_user.groups.add(gr)
        toke = get_token_for_user(my_user)
        return Response({'msg':toke},status=status.HTTP_200_OK)

class UserSiginInViews(APIView):
    render_classes = [UserRenderers]
    def post(self,request,format=None):
        serializers = UserLoginSerializers(data=request.data, partial=True)
        if serializers.is_valid(raise_exception=True):
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                tokens = get_token_for_user(user)
                return Response({'token':tokens,'message':'Tizimga xush kelibsiz'},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'none_filed_error':['Bunday foydalanuvchi tizimga mavjud emas']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class UpdatePhoneUpdateView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def put(self,request,pk,appSignature,format=None):
        data = request.data
        serializers = UserUpdateSerializers(instance=CustumUsers.objects.filter(id=pk)[0] ,data=data,partial =True,context={'user_id':request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            us = CustumUsers.objects.filter(id=pk)[0]
            code_s = str(random.randint(10000,99999))
            us.code_s=code_s
            us.save()
            print(us.username)
            send_message(us.username,code_s,appSignature)
            return Response({"msg":'Saqlandi'},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class UserUpdateFullNameViews(APIView):
    def put(self,request,pk,format=None):
        data = request.data
        serializers = UpdateFullNameSerializers(instance=CustumUsers.objects.filter(id=pk)[0] ,data=data,partial =True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({"msg":'Yangilandi'},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class CheckSms(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def post(self,request):
        code = request.data['code_s']
        if code =='':
            context = {"Kod Kiritilmadi"}
            return Response(context,status=status.HTTP_401_UNAUTHORIZED)
        user = CustumUsers.objects.filter(id=request.user.id)[0]
        if code==user.code_s:
            context={'Tizimga xush kelibsiz'}
            return Response(context,status=status.HTTP_200_OK)
        else:
            return Response({'error':'parol xato'})

class UserProfilesViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):  
        serializer = UserPorfilesSerializers(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)


class ClientCreateViews(APIView):
    def get(self,request,format=None):
        clients = CustumUsers.objects.filter(groups__in = ['Client'])
        serializers = UserPorfilesSerializers(clients,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def post(self,request,format=None):
        try:
            get_shops = Shops.objects.get(user_id = request.user.id)
        except Shops.DoesNotExist:
            get_shops = None
        serializers = UserUpdateSerializers(data= request.data,context={'user_id':get_shops})
        if serializers.is_valid(raise_exception = True):
            serializers.save()
            return Response({'msg':"Klient qo'shildi"},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ClientsUpdateViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,pk,format=None):
        shop = CustumUsers.objects.filter(id=pk)
        serializers = UserPorfilesSerializers(shop,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):
        try:
            get_shops = Shops.objects.get(user_id = request.user.id)
        except Shops.DoesNotExist:
            get_shops = None
        serializers = UserUpdateSerializers(instance=CustumUsers.objects.filter(id=pk)[0],data=request.user.id,partial =True,context={'user_id':get_shops})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':"success update"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)
    
class ClientsUpdateShopViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,pk,format=None):
        shop = get_object_or_404(CustumUsers,username = int(pk))
        serializers = UserPorfilesSerializers(shop)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):
        data = request.data
        serializers = ClientUserUpdateSerializers(instance=CustumUsers.objects.filter(username = int(pk))[0],data=data,partial =True,context={'shops_id':request.user.shops_id})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':"success update"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)

class ShopsClientViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request):
        shop = Shops.objects.get(user_id=request.user.id)
        print(shop)
        user = CustumUsers.objects.filter(shops_id=shop.id)
        serializers = ShopsClientSerializers(user,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)



