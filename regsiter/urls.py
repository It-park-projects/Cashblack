from django.urls import path
from regsiter.views import *


urlpatterns = [
    path('',sigin_in,name='sigin_in'),
    path('logout_user/',logout_user,name='logout_user'),
    path('home_admin/',home_admin,name='home_admin'),
    path('static_information/',static_information,name='static_information'),
    path('billing_sistem/',billling_sistem,name='billing_sistem'),
    path('create_billing_summ/<int:pk>/',CreateSummPayment.as_view(),name='create_billing_summ'),
    path('billing_info_shops/<int:id>/',billing_info_shops,name='billing_info_shops'),
    path('create_summ_shops/',create_summ_shops,name='create_summ_shops'),
    # Catgeor views
    path('all_ctageor/',all_ctageor,name='all_ctageor'),
    path('create_categor/',CreateCategorViews.as_view(),name='create_categor_views'),
    path('update_catgeor/<int:pk>/',UpdateCategorViews.as_view(),name='update_catgeor'),
    path('delete_categor/<int:pk>/',DeleteCategorViews.as_view(),name='delete_categor'),

    # notification
    path('notification_admin/',notification_admin,name='notification_admin')
]