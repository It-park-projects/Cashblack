from django.urls import path
from register.views import *


urlpatterns = [
    path('',sigin_in,name='sigin_in'),
    path('logout_user/',logout_user,name='logout_user'),
    path('home_admin/',home_admin,name='home_admin'),
    path('static_information/',static_information,name='static_information'),
    path('billing_sistem/',billling_sistem,name='billing_sistem'),
    # Catgeor views
    path('all_ctageor/',all_ctageor,name='all_ctageor'),
    path('create_categor/',CreateCategorViews.as_view(),name='create_categor_views'),
    path('update_catgeor/<int:pk>/',UpdateCategorViews.as_view(),name='update_catgeor'),
    path('delete_categor/<int:pk>/',DeleteCategorViews.as_view(),name='delete_categor')
]