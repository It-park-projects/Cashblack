from django.urls import path
from authen.views import *

urlpatterns = [
    path('all_groups_users/',AllGroupsViews.as_view()),
    path('user_sigin_up_views/<str:appSignature>/',UserSiginUpViews.as_view()),
    path('user_sigin_in_views/',UserSiginInViews.as_view()),
    path('user_profiles_views/',UserProfilesViews.as_view()),
    path('user_phone_update/<int:pk>/<str:appSignature>/',UpdatePhoneUpdateView.as_view()),
    path('user_update_fullname/<int:pk>/',UserUpdateFullNameViews.as_view()),
    path('create_clients/',ClientCreateViews.as_view()),
    path('update_clients/<int:pk>/',ClientsUpdateViews.as_view()),
    path('update_clients_shop/<str:pk>/',ClientsUpdateShopViews.as_view()),
    path('shop_client_views/',ShopsClientViews.as_view()),
    path('check_sms/',CheckSms.as_view()),


    path('create_sotrutnik_view/',CreateSotrutnikView.as_view()),
    path('delete_sotrutnik/<int:pk>/',DeleteSotrutnik.as_view()),
    path('create_client_view/<str:appSignature>/',CreateClientView.as_view()),
]