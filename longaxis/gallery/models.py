from django.db import models
from django.shortcuts import reverse
from users.models import User
from taggit.managers import TaggableManager
from datetime import datetime
from django.conf import settings
import random
import os
# Create your models here.

def user_directory_path(instance, filename):
    basename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(6))
    _now = datetime.now()

    return 'gallery/{username}/{year}/{month}/{day}/{basename}{randomstr}{ext}'.format(
        username = instance.user.username,
        year = _now.strftime('%Y'),
        month = _now.strftime('%m'),
        day = _now.strftime('%d'),
        basename = basename,
        randomstr = randomstr,
        ext = file_extension,
        )

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='title',blank=False)
    image = models.ImageField(upload_to=user_directory_path, verbose_name='photo', null=False)
    description = models.TextField(max_length=300, verbose_name='description', blank=True)
    date_posted = models.DateTimeField(auto_now_add = True)
    tags = TaggableManager(blank=True)
    likes = models.ManyToManyField(User, blank=True, default=None, related_name='likes', through='LikePhoto')
    def __str__(self):
        return f"[{self.pk}]{self.title}"
    
    def get_absolute_url(self):
        return reverse('gallery:detail' , args=[str(self.pk)])

    def total_likes(self):
        return self.likes.count()

    class Mete:
        ordering = ['-date_posted']

    #django-claenup 에서 대신해줌
    # def delete(self, *args, **kargs):
    #     if self.image:
    #         os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
    #     super(Photo, self).delete(*args, **kargs)

class LikePhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user} likes {self.photo.title}"
    
    class Meta:
        ordering = ['-date_added']

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.CharField(max_length=300, verbose_name='comment_text', blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True,blank=True, related_name='sub_comment', default=None)

    def __str__(self):
        return f"[photo_pk{self.parent_photo.id}] {self.user}'s comment"


