from django.contrib import admin
from .models import *

# Register your models here.

class UserDataAdmin(admin.ModelAdmin):
    list_display=('user_name','user_mail','gender','age','password')


admin.site.register(UserData,UserDataAdmin)