import requests
import random
from rest_framework.response import Response
from rest_framework import status,authentication,permissions,filters
from django.contrib.auth import authenticate,login,logout
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.decorators import api_view,parser_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,Group
from django.contrib.auth import logout
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
    def post(self,request):
        username = request.data['username']
        password= request.data['password']
        if username == "":
            context = {"Tel Raqam Kiritilmadi"}
            return Response(context,status=status.HTTP_401_UNAUTHORIZED)
        us = CustumUsers.objects.filter(username=username)
        if len(us)!=0:
            return Response({'error':"Telefon raqam mavjud"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)      
        my_user = CustumUsers.objects.create(username=username)
        my_user.set_password(password)
        my_user.save()
        toke =get_token_for_user(my_user)   
        return Response({'msg':toke},status=status.HTTP_200_OK)
    def put(self,request):
        us = CustumUsers.objects.filter(id=request.user.id)[0]
        code_s = str(random.randint(10000,99999))
        us.code_s=code_s
        us.save()
        send_message(us.username,us.code_s)
        return Response({'message':'send_sms'})
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
                return Response({'token':tokens,'message':'Login success'},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'none_filed_error':['Email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class UpdatePhoneUpdateView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def put(self,request,pk,format=None):
        data = request.data
        serializers = UserUpdateSerializers(instance=CustumUsers.objects.filter(id=pk)[0] ,data=data,partial =True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            us = CustumUsers.objects.filter(id=pk)[0]
            code_s = str(random.randint(10000,99999))
            us.code_s=code_s
            us.save()
            send_message(us.username,us.code_s)
            return Response({"msg":'Saved'},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class UserUpdateFullNameViews(APIView):
    def put(self,request,pk,format=None):
        data = request.data
        serializers = UserUpdateSerializers(instance=CustumUsers.objects.filter(id=pk)[0] ,data=data,partial =True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({"msg":'Saved'},status=status.HTTP_200_OK)
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
            context={'success'}
            return Response(context,status=status.HTTP_200_OK)
        else:
            return Response({'error':'parol xato'})

class UserProfilesViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserPorfilesSerializers(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)