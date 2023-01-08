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
from rest_framework.parsers import JSONParser,FileUploadParser,MultiPartParser, FormParser
from regsiter.models import *
from billing.models import *
from billing.serializers import *
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta, datetime
import requests
import json
import base64
from billing.uzcard_settings import *



class MyBlance(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        balans =  Balans.objects.filter(shop_id__user_id=request.user.id)
        print(balans)
        serializers = BalanceSerializers(balans,many=True)
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
    # parser_classes = (FileUploadParser, MultiPartParser, FormParser,JSONParser)
    def get(self,request,format=None):
        notification = NotifikationsSendClient.objects.filter(user_id=request.user.id)
        serializers = AllNotificationSmsSerializers(notification,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def post(self,request,format=None):
        # shop = Shops.objects.get(user_id=request.user.id)
        shop = get_object_or_404(Shops,user_id=request.user.id) 
        serializers = CreateNotificationSmsSerializers(data=request.data,context={'user_id':request.user,'shop_id':shop,'users_id':request.user.id})
        if serializers.is_valid(raise_exception = True):
            serializers.save(
                img = request.data.get('img')
            )
            return Response({'msg':"Send notifications"},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    

class AllClientNotificationView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        ls = []
        for item in request.user.shops_id.all():
            for i in NotifikationsSendClient.objects.filter(status_id=3):
                if i.shop_id.id == item.id:
                    ls.append({'id':i.id,'title':i.title,'content':i.content,'img':i.img.url,})
        # serializers = AllNotificationSmsSerializers(notification,many=True)
        return Response(ls,status=status.HTTP_200_OK)


class SendNotificationForUserViews(APIView):
    def get(self,request,format=None):
        try:
            get_users_payment_date = Balans.objects.get(user_id=request.user.id)
        except Balans.DoesNotExist:
            get_users_payment_date = None
        get_day = (get_users_payment_date.payment_date + relativedelta(months=1))-relativedelta(days=3)
        if date.today().day == get_day.day and date.today().month == get_day.month:
            return Response({"msg":"Iltimos Blansni oldindan to'ldirib qo'ying"})
        return Response({'msg':"sdsdsd"})


class PaymentSendCard(APIView):
    render_classes = [UserRenderers]    
    perrmisson_class = [IsAuthenticated]
    
    usrPass = "texnolike:myuU3te4N01!KE"
    data_bytes = usrPass.encode("utf-8")
    b64Val = base64.b64encode(data_bytes)
    def post(self,request):
        card_number = request.data['card_number']
        expire_date = request.data['expire_date']
        amount = request.data['amount']
        shops = Shops.objects.get(user_id=request.user.id)
        if card_number == '' or expire_date=='' or amount=='':
            return Response({'error':"Ma'lumotlarni to'ldiring"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        if int(shops.payment_summ) >= int(amount):
             return Response({'error':"Eng kam miqdor" + ' ' + shops.payment_summ + ' ' + "Bo'lishi kerak"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        code_s = str(random.randint(10000,99999))
        url = "https://pay.myuzcard.uz/api/Payment/paymentWithoutRegistration"
        token = b64Val
        payload = json.dumps({
            "amount": f"{amount}",
            "cardNumber": f"{card_number}",
            "expireDate": f"{expire_date}",
            "extraId": f"{code_s}"

        })
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Basic'+" "+token.decode('utf-8'),
            'Content-Type': 'application/json'
        }
        response = requests.post(url,  headers=headers, data=payload)
        x = json.loads(response.text)
        return Response({'msg':x},status=status.HTTP_200_OK)

class PaymentConfirmCard(APIView):
    render_classes = [UserRenderers]    
    perrmisson_class = [IsAuthenticated]
    def post(self,request):
        card_number = request.data['card_number']
        expire_date = request.data['expire_date']
        amount = request.data['amount']
        session = request.data['session']
        otp = request.data['otp']
        if session == '' or otp=='':
            return Response({'error':"Ma'lumotlarni to'ldiring"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        confirmUserCard(session,otp)
        for item in request.user.shops_id.all():
            x = item
        my_user = PaymentHistory.objects.create(card_number=card_number,expire_date=expire_date,amount=amount,extra_id=session,user_id=request.user,shop_id=x)
        my_user.save()
        history = PaymentHistory.objects.filter(shop_id=x).last()
        balans = Balans.objects.filter(shop_id=x)[0]
        b = int(balans.amunt)+int(amount)
        balans.shop_id=history.shop_id
        balans.amunt=str(b)
        balans.payment_id=history
        balans.save()
        # shop = Shops.objects.filter(shop_id=x).update(is_payment=True)
        return Response({'msg':'Tolov qabul qilindi'},status=status.HTTP_200_OK)

class HistoryPayment(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request):
        history =  PaymentHistory.objects.filter(user_id=request.user.id)
        serializers = HistoryPamentSerialzers(history,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)


class CloseBalance(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request):
        data = request.user
        get_amount =  Balans.objects.filter(shop_id__user_id=request.user.id)

        print(get_amount)
        # add_month = get_amount.payment_date + relativedelta(months=1)
        # get_shop = Shops.objects.filter(user_id=request.user.id)[0]
        # if datetime.today().strftime('%Y-%m-%d') >= add_month.strftime('%Y-%m-%d') and get_shop.is_payment == True:
        #     get_shop1 = Shops.objects.filter(user_id=request.user.id).update(is_payment = False)
        return Response({"msg":False})
