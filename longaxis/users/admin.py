from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

class UserAdmin(UserAdmin):
    list_display = ('email','username','date_joined')
    list_filter = ('is_admin',)

    readonly_fields= ('date_joined', 'last_login')

    ordering = ('-date_joined',)

    #useradmin 필수
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
