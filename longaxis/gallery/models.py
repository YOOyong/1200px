from django.db import models
from users.models import User
from taggit.managers import TaggableManager
# Create your models here.

def user_directory_path(instance, filename):
    #this file will be uploaded to MEDIA_ROOT /user_id/post id
    return '{}/{}'.format(instance.username, filename)


class Photo(models.Model):
    photographer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    photo = models.ImageField(upload_to=user_directory_path, verbose_name='Photo', null=False)
    date_posted = models.DateField(auto_now_add = True)
    tags = TaggableManager(blank=True)
    likes = models.IntegerField()   

    def __str__(self):
        return self.title


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='photo_likes')

    


    

    


