from unicodedata import category
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
from shops.serializers import *
from authen.serializers import *


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
        serializers = ShopsSerializers(data=request.data,context={'user_id':request.user})
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
        serializers = ShopsSerializers(instance=Shops.objects.filter(id=pk)[0],data=request.user.id,partial =True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':"success update"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)

class ClientCreateViews(APIView):
    def get(self,request,format=None):
        clients = CustumUsers.objects.filter(groups__in = ['Client'])
        serializers = ClientSerializers(clients,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def post(self,request,format=None):
        serializers = CustomUserClientsSerializers(data= request.data)
        if serializers.is_valid(raise_exception = True):
            serializers.save()
            return Response({'msg':'Create Sucsess'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)