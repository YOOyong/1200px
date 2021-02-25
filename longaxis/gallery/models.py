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

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('gallery:detail' , args=[str(self.id)])

    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(Photo, self).delete(*args, **kargs)

    


# class Likes(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
#     photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='photo_likes')

    


    

    


