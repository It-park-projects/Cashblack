from django.contrib import admin
from billing.models import *

admin.site.register(Balans)
admin.site.register(NotifikationsSendClient)
admin.site.register(NotificationStatus)
admin.site.register(PaymentHistory)