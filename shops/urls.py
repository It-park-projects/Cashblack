from django.urls import path
from shops.views import *


urlpatterns = [
    path('shops_views/',UserShops.as_view()),
    path('all_categor_views/',AllCategorViews.as_view()),

]