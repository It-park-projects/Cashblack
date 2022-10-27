from atexit import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from regsiter.models import *
from regsiter.forms import *


class NewMyUser(UserAdmin):
    add_form = CreasteUser
    form = ChangeUser
    model = CustumUsers
    list_display = ['username','first_name','last_name','id',]
    fieldsets = UserAdmin.fieldsets + (
        (None,{'fields':('code_s','shops_id',)}),
    )
    add_fieldsets = (
        (None,{'fields':('username','password1','password2')}),
    )
admin.site.register(CustumUsers,NewMyUser)

admin.site.register(Cataegor)
admin.site.register(Distric)
admin.site.register(Province)
admin.site.register(Shops)
