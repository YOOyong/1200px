from django.db import models

# Create your models here.
class Account(models.Model):
    
    email = models.EmailField(verbose_name='이메일', unique=True)
    nickname = models.CharField(verbose_name='닉네임', max_length=20,  unique=True)
    profile_image = models.ImageField(verbose_name='프로필사진')
    password = models.CharField(max_length=128, verbose_name='비밀번호')
    introduce = models.TextField(max_length=500, verbose_name='소개')
    registered_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nickname

    class Meta:
        db_table='account'
        verbose_name='계정'
        verbose_name_plural='계정'

