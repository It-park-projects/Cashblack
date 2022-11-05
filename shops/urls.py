from django.urls import path
from shops.views import *


urlpatterns = [
    path('shops_views/',UserShops.as_view()),
    path('shops_update_view/<int:pk>/',ShopsUpdateViews.as_view()),
    path('all_categor_views/',AllCategorViews.as_view()),
    path('all_province_view/',AllProvinceViews.as_view()),
    path('all_distrik_view/',AllDistricViews.as_view()),
    path('cashbak_create/<int:barcode_id>/<str:is_cashback>/',ClientSellView.as_view()),
    path('client_statistic_view/',ClientStatistikaView.as_view()),
]