from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from register.models import *

class UserLoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = ['username',]