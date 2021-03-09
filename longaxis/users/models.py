from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image
import random
import os
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):

        if not email:
            raise ValueError('user must have an email')
        if not username:
            raise ValueError('user must have a name')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):

        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email',
                              max_length=255, unique=True)
    username = models.CharField(
        verbose_name='username', max_length=20, unique=True)
    date_joined = models.DateField(default=timezone.now)
    last_login = models.DateField(auto_now=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def total_following(self):
        return self.following.count()

    def total_followers(self):
        return self.followers.count()


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


def user_directory_path(instance, filename):
    basename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(6))

    return 'profile/{username}/{basename}{randomstr}{ext}'.format(
        username=instance.user.username,
        basename=basename,
        randomstr=randomstr,
        ext=file_extension,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        blank=True, null=True, default='profile/default_profile.jpg', upload_to=user_directory_path)
    state_message = models.CharField(max_length=100, blank=True)
    intro = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args,**kwargs):
        super().save()
        img = Image.open(self.profile_image.path)

        if img.height > img.width:
            left = 0
            right = img.width
            top = (img.height - img.width) / 2
            bottom = (img.height + img.width) /2
            img = img.crop((left,top,right, bottom))

        if img.height < img.width:
            left = (img.width - img.height) / 2
            right = (img.width + img.height) / 2
            top = 0
            bottom = img.height
            img = img.crop((left,top,right,bottom))

        if img.height > 300 or img.width > 300:
            img = img.resize((300,300), Image.ANTIALIAS)
            img.save(self.profile_image.path, quality=90)



# user의 save()가 실행될 때  profile도 save() 실행되도록 함
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)