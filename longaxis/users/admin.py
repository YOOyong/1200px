from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','username','date_joined')
    list_filter = ('is_admin')

    search_fields = ('username',)

    ordering('date_joined')

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
