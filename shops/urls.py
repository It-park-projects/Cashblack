from django.urls import path
from shops.views import *


urlpatterns = [
    path('shops_views/',UserShops.as_view()),
    path('shops_update_view/<int:pk>/',ShopsUpdateViews.as_view()),
    path('all_categor_views/',AllCategorViews.as_view()),
    path('all_province_view/',AllProvinceViews.as_view()),
    path('all_distrik_view/',AllDistricViews.as_view()),
    path('cashbak_create/<int:barcode_id>/<str:is_cashback>/',ClientSellView.as_view()),
    path('statistics_today/',StatisticsTodayCashbacks.as_view()),
    path('statistics_yestarday/',StatisticsYestardayCashbacks.as_view()),
    path('statistics_before_yestarday/',StatisticsBeforeYestardayCashbacks.as_view()),
    path('statistics_month/',StatisticsMonthCashbacks.as_view()),
    path('statistics_before_month/',StatisticsBeforeMonthCashbacks.as_view()),
    path('statistics_before_3_month/',StatisticsBefore3MonthCashbacks.as_view()),
    path('statistics_year/',StatisticsYearCashbacks.as_view()),
]