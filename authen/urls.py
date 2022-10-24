from django.urls import path
from authen.views import *

urlpatterns = [
    path('all_groups_users/',AllGroupsViews.as_view()),
    path('user_sigin_up_views/',UserSiginUpViews.as_view()),
    path('user_sigin_in_views/',UserSiginInViews.as_view()),
    path('user_profiles_views/',UserProfilesViews.as_view()),
    path('user_phone_update/<int:pk>/',UpdatePhoneUpdateView.as_view()),
    path('user_update_fullname/<int:pk>/',UserUpdateFullNameViews.as_view()),
    path('check_sms/',CheckSms.as_view())
]