from django.contrib import admin
from .models import Photo, Comment, LikePhoto
# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment
    can_delete = True
    verbose_name_plural= 'comments'
    ordering = ('-date_posted',)
    fk_name = 'parent_photo'

class LikeInline(admin.StackedInline):
    model = LikePhoto
    can_delete = True
    verbose_name_plural= 'likes'
    ordering = ('-date_added',)
    fk_name = 'photo'


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user','date_posted',)
    ordering = ('-date_posted',)
    inlines = (LikeInline,CommentInline,)

    def get_inline_instances(self, request, obj = None):
        if not obj:
            return list()
        
        return super(PhotoAdmin, self).get_inline_instances(request,obj)

admin.site.register(Photo, PhotoAdmin)