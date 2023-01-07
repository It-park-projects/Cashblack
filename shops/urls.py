from django.urls import path
from shops.views import *


urlpatterns = [
    path('shops_views/',UserShops.as_view()),
    path('shops_update_view/<int:pk>/',ShopsUpdateViews.as_view()),
    # path('update_shops/<int:id>/',update_shops),
    path('all_categor_views/',AllCategorViews.as_view()),
    path('all_province_view/',AllProvinceViews.as_view()),
    path('all_distrik_view/',AllDistricViews.as_view()),

    path('client_category/',ClientCategory.as_view()),
    path('client_shops/<int:pk>/',ClientShops.as_view()),
    path('client_shops_statistics/<int:id>/',ClientShopsStatistics.as_view()),
    path('client_shop_filter/<int:id>/<str:start_date>/<str:end_date>/',ClientShopStatisticsGet.as_view()),

    path('cashbak_create/<int:barcode_id>/<str:is_cashback>/',ClientSellView.as_view()),
    
    path('cashback_one_month_statistics/',StatisticsTodayCashbacks.as_view()),
    path('cashbacks_filter_statistics/<str:start_date>/<str:end_date>/',StatisticsCashbacksFilter.as_view()),

    path('statistics_summa/',StatistikaSumma.as_view())
    

]