from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("Users must have an username")
        if not email:
            raise ValueError("User must have an email")
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    username = models.CharField(unique=True,max_length=30)
    email = models.CharField(unique=True,max_length=30)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [ 'email',]

    objects = MyAccountManager()

    def __str__(self):
        return "("+str(self.username)+")"+str(self.email)
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True