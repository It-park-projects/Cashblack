from django.urls import path
from billing.views import *

urlpatterns = [
    path('my_blance/',MyBlance.as_view()),
]