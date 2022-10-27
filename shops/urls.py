from django.urls import path
from shops.views import *


urlpatterns = [
    path('shops_views/',UserShops.as_view()),
    path('shops_update_view/<int:pk>/',ShopsUpdateViews.as_view()),
    path('all_categor_views/',AllCategorViews.as_view()),
    path('all_province_view/',AllProvinceViews.as_view()),
    path('all_distrik_view/',AllDistricViews.as_view()),
    path('create_clients/',ClientCreateViews.as_view()),
    path('update_clients/<int:pk>/',ClientsUpdateViews.as_view()),

    

]