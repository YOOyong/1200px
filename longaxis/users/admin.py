from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class UserAdmin(UserAdmin):
    list_display = ('email','username','date_joined')
    list_filter = ('is_admin',)

    readonly_fields= ('date_joined', 'last_login')

    ordering = ('-date_joined',)

    #useradmin 필수
    filter_horizontal = ()
    fieldsets = ()

    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj = None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
