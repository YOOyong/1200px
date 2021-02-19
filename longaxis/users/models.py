from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('user must have an email')
        if not username:
            raise ValueError('user must have a name')
        
        user = self.model(
            email= self.normalize_email(email),
            username= username,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
        

    def create_superuser(self, email, username, password):
        
        user = self.create_user(
            eamil= email,
            username= username,
        )
        user.is_admin= True
        user.save(using= self._db)
        
        return user

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name='email', max_length=100, unique=True)
    username = models.CharField(verbose_name='username', max_length=20, unique=True, blank = False)
    date_joined = models.DateField(default=timezone.now())

    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [username,]

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

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
