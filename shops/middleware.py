from django.shortcuts import redirect, render
from regsiter.models import *
from shops.models import *

def get_shops_user(get_res):
    def middleware(request):
        request.get_shop = Shops.objects.all()
        response = get_res(request)

        return response
    return middleware