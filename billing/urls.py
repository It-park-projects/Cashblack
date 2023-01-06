from django.urls import path
from billing.views import *

urlpatterns = [
    path('my_blance/',MyBlance.as_view()),
    path('all_notification_views/',AllNotificationsViews.as_view()),
    path('allClient_notification_view/',AllClientNotificationView.as_view()),
    path('notification/',SendNotificationForUserViews.as_view()),

    path('payment_send_card/',PaymentSendCard.as_view()),
    path('payment_confirm_card/',PaymentConfirmCard.as_view()),
    
]