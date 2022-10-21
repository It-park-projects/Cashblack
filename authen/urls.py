from django.urls import path
from authen.views import *

urlpatterns = [
    path('user_sigin_up_views/',UserSiginUpViews.as_view()),
]