from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,Group, PermissionsMixin)

from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from rest_framework_simplejwt.tokens import RefreshToken
from django.dispatch import receiver
from tallyapp.models import companydata,ladgernamedata

# from sorl.thumbnail import ImageField,get_thumbnail
# from PIL import Image, ImageFont, ImageDraw,


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        # username = self.model.normalize_username(username)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user



class User(AbstractBaseUser, PermissionsMixin):
    # username = models.CharField(max_length=255, unique=True, db_index=True)
    name=models.CharField(max_length=50,blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    mobile=models.CharField(max_length=12,blank=True, null=True)
    Otheruser_type = (
        ("CA", "CA"),
        ("Accountant", "Accountant"),
    )
    type = models.CharField(max_length=20, choices=Otheruser_type,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_delete = models.BooleanField(null=True)
    is_edit = models.BooleanField(null=True)
    is_views = models.BooleanField(null=True)
    created_by=models.CharField(max_length=50,blank=True, null=True)
    # groups = models.ForeignKey(Group,blank=True,null=True,on_delete=models.DO_NOTHING)
    port_num=models.CharField(max_length=50,blank=True, null=True,default='9000')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # auth_provider = models.CharField(
    #     max_length=255, blank=False,
    #     null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    # REQUIRED_FIELDS = ['email']
    objects=UserManager()
    def __str__(self):
        return self.email
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }    
class PpOrgnM(models.Model):
    usr = models.ForeignKey(User, models.CASCADE)
    orgn_nm = models.ForeignKey(companydata,on_delete=CASCADE,null=True,blank=True)
    orgn_email = models.CharField(max_length=320, blank=True, null=True)
    orgn_mobile = models.PositiveIntegerField(blank=True, null=True)
    orgn_address=models.TextField(blank=True,null=True)
    orgn_website=models.CharField(max_length=100,blank=True,null=True)
    orgn_state = models.CharField(max_length=40, blank=True, null=True)
    orgn_gstin = models.CharField(max_length=40, blank=True, null=True)
    vat_no=models.CharField(max_length=100,null=True,blank=True)
    cst_no=models.CharField(max_length=100,null=True,blank=True)
    pan_no=models.CharField(max_length=100,null=True,blank=True)
    
    entr_by = models.CharField(blank=True, null=True,max_length=50)
    entr_dt = models.DateTimeField(blank=True, null=True)
    ip_addr = models.CharField(max_length=16, blank=True, null=True)
    mac_addr = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return str(self.orgn_nm)

    @property
    def bnklist(self):
        return self.ppbnkm_set.all()    
