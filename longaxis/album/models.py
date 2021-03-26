from django.db import models
from users.models import User
from gallery.models import Photo
from django.shortcuts import reverse

# Create your models here.
class UserAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    album_photos = models.ManyToManyField(Photo, through='AlbumPhoto')
    album_name = models.CharField(max_length=50, blank=False)
    is_private = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user}'s album [{self.album_name}]"

    def get_absolute_url(self):
        return reverse('album:album', args=[self.user, str(self.id)])

class AlbumPhoto(models.Model):
    album = models.ForeignKey(UserAlbum, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.photo} is in {self.album}"

    class Meta:
        ordering = ['-date_added']