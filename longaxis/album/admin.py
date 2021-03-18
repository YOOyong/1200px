from django.contrib import admin
from .models import UserAlbum, AlbumPhoto

# Register your models here.
class AlbumPhotoInline(admin.TabularInline):
    model = AlbumPhoto
    extra = 2 # how many rows to show

class UserAlbumAdmin(admin.ModelAdmin):
    model= UserAlbum
    list_display = ('album_name','user','date_created')
    inlines = (AlbumPhotoInline, )

admin.site.register(UserAlbum ,UserAlbumAdmin)