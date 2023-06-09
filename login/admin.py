from django.contrib import admin
from .models import *

# Register your models here.

class UserDataAdmin(admin.ModelAdmin):
    list_display=('user_name','user_mail','gender','age','password')

class SessionAdmin(admin.ModelAdmin):
    list_display=('session_key','host_id','host_name','end_time')

class SessionLogAdmin(admin.ModelAdmin):
    list_display=('session_key','user','mr','ear','time_ms')

class session_members_admin(admin.ModelAdmin):
    list_display=('session_key','user_id','user','permission')

admin.site.register(session_members,session_members_admin)

admin.site.register(sessionLog,SessionLogAdmin)

admin.site.register(Session,SessionAdmin)

admin.site.register(UserData,UserDataAdmin)

