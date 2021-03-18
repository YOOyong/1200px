from django.contrib import admin
from .models import Photo, Comment, UserAlbum, AlbumPhoto
# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment
    can_delete = True
    verbose_name_plural= 'comments'
    ordering = ('-date_posted',)
    fk_name = 'parent_photo'

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user','date_posted',)
    ordering = ('-date_posted',)
    inlines = (CommentInline, )

    def get_inline_instances(self, request, obj = None):
        if not obj:
            return list()
        
        return super(PhotoAdmin, self).get_inline_instances(request,obj)

class AlbumPhotoInline(admin.TabularInline):
    model = AlbumPhoto
    extra = 2 # how many rows to show

class UserAlbumAdmin(admin.ModelAdmin):
    model= UserAlbum
    list_display = ('album_name','user','date_created')
    inlines = (AlbumPhotoInline, )

admin.site.register(Photo, PhotoAdmin)
admin.site.register(UserAlbum ,UserAlbumAdmin)