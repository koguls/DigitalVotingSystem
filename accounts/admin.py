from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomerUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + ((None, {'fields' : ('role',)}),)
admin.site.register(CustomUser, CustomerUserAdmin)

