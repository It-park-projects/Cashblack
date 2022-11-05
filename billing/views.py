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
from authen.servise import send_message
from regsiter.models import *
from billing.models import *
from billing.serializers import *


class MyBlance(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        blance =  Blance.objects.filter(user_id=request.user.id)
        serializers = BalanceSerializers(blance,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        shop = Shops.objects.get(user_id=request.user.id)
        serializers = CreateBillingsSerializer(data=request.data,context={'user_id':request.user,'shop_id':shop})
        if serializers.is_valid(raise_exception = True):
            serializers.save()
            return Response({'msg':"To'lov qabul qilindi"},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class AllNotificationsViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        notification = NotifikationsSendClient.objects.filter()
        serializers = AllNotificationSmsSerializers(notification,many=True)
        return Response()