from atexit import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from register.models import *
from register.forms import *


class NewMyUser(UserAdmin):
    add_form = CreasteUser
    form = ChangeUser
    model = CustumUsers
    list_display = ['phone','first_name','last_name','id',]
    fieldsets = UserAdmin.fieldsets + (
        (None,{'fields':('phone',)}),
    )
    add_fieldsets = (
        (None,{'fields':('phone','password1','password2')}),
    )
admin.site.register(CustumUsers,NewMyUser)

admin.site.register(Cataegor)