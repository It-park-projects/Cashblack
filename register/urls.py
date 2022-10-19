from django.urls import path
from register.views import *


urlpatterns = [
    path('',sigin_in,name='sigin_in'),
    path('logout_user/',logout_user,name='logout_user'),
    path('home_admin/',home_admin,name='home_admin'),
    path('static_information/',static_information,name='static_information'),
    path('billing_sistem/',billling_sistem,name='billing_sistem'),
    path('all_ctageor/',all_ctageor,name='all_ctageor'),
]