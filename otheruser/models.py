from django.db import models
from django.db.models.base import Model
from django.db.models.fields import AutoField
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,Group, PermissionsMixin)

from django.db import models
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.dispatch import receiver

# Create your models here.

class OtheruserManager(BaseUserManager):
    def create_user(self, Otheruser_email, Otheruser_pass, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not Otheruser_email:
            raise ValueError('The given email must be set')
        Otheruser_email = self.normalize_email(Otheruser_email)
        # username = self.model.normalize_username(username)
        user = self.model(Otheruser_email=Otheruser_email, **extra_fields)
        user.set_password(Otheruser_pass)
        user.save(using=self._db)
        return user

class Otheruser(AbstractBaseUser):
    Otheruser_name=models.CharField(max_length=100)
    Created_user=models.CharField(max_length=100)
    Otheruser_email=models.EmailField()
    Otheruser_add=models.CharField(max_length=200)
    Otheruser_mobile=models.CharField(max_length=15)
    Otheruser_type = (
    ("CA", "CA"),
    ("Accountant", "Accountant"),
    )
    Type = models.CharField(max_length = 20, choices = Otheruser_type )
    is_verified=models.BooleanField(default=False)
    Is_delete = models.BooleanField()
    Is_edit = models.BooleanField()
    Is_views = models.BooleanField()
    Otheruser_pass=models.CharField(max_length=10)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'Otheruser_email'
    # REQUIRED_FIELDS = ['username']

    # REQUIRED_FIELDS = ['email']
    objects=OtheruserManager()

    def __str__(self):
        return self.Otheruser_email
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }    
   

