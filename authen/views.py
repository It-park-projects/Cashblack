from rest_framework.response import Response
from rest_framework import status,authentication,permissions,filters
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
import requests
from authen.renderers import UserRenderers
from authen.serializers import UserLoginSerializers
from register.models import CustumUsers


# token Olish
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'accsess':str(refresh.access_token)
    }


class UserSiginUpViews(APIView):
    render_classes = [UserRenderers]
    def post(self,request,format=None):
        serializers = UserLoginSerializers(data=request.data, partial=True)

        if serializers.is_valid(raise_exception=True):
            username = serializers.data['username']
            user_check = CustumUsers.objects.filter(username=username)
            if len(user_check)!=0:

                url = "http://91.204.239.44/broker-api/send"
                params = {
                    "messages":
                         [
                         {
                          "recipient":f"{username}",
                          "message-id":"abc000000001",

                             "sms":{
                        
                               "originator": "3700",
                             "content": {
                              "text": "Salom"
                              }
                              }
                                 }
                             ]
                        }
            username = "assistant"
            password = "rA@8e3vE)@3X"
            response = requests.post(url, auth=(username, password), json=params)
            print(response)
        return Response(status=status.HTTP_204_NO_CONTENT)