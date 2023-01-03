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
from dateutil.relativedelta import relativedelta
from datetime import date


class MyBlance(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        blance =  Blance.objects.filter(user_id=request.user.id)
        serializers = BalanceSerializers(blance,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        shop = Shops.objects.get(user_id=request.user.id)
        user_change_staff = CustumUsers.objects.filter(id = request.user).update(is_staff = True)
        serializers = CreateBillingsSerializer(data=request.data,context={'user_id':request.user,'shop_id':shop})
        if serializers.is_valid(raise_exception = True):
            serializers.save()
            return Response({'msg':"To'lov qabul qilindi"},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class AllNotificationsViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        notification = NotifikationsSendClient.objects.filter(author_id=request.user.id)
        serializers = AllNotificationSmsSerializers(notification,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def post(self,request,format=None):
        shop = Shops.objects.get(user_id=request.user.id)
        serializers = CreateNotificationSmsSerializers(data=request.data,context={'author_id':request.user,'shop_id':shop,'status_id':1})
        if serializers.is_valid(raise_exception = True):
            serializers.save()
            return Response({'msg':"Send notifications"},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    

class AllClientNotificationView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        for item in request.user.shops_id.all():
            x = item.id
        notification = NotifikationsSendClient.objects.filter(shop_id=x,status_id=3)
        serializers = AllNotificationSmsSerializers(notification,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)


class SendNotificationForUserViews(APIView):
    def get(self,request,format=None):
        try:
            get_users_payment_date = Blance.objects.get(user_id=request.user.id)
        except Blance.DoesNotExist:
            get_users_payment_date = None
        get_day = (get_users_payment_date.payment_date + relativedelta(months=1))-relativedelta(days=3)
        if date.today().day == get_day.day and date.today().month == get_day.month:
            return Response({"msg":"Iltimos Blansni oldindan to'ldirib qo'ying"})
        return Response({'msg':"sdsdsd"})
