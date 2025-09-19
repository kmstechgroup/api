from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
        list_display = ['id_user', 'email', 'password', 'first_name', 'last_name']
        fields = ['email', 'first_name', 'last_name', 'password']
#admin.site.register(User)
