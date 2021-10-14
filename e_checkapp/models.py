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


# class UserManager(BaseUserManager):
#     def create_user(self, email, password, **extra_fields):
#         """
#         Create and save a user with the given username, email, and password.
#         """
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         # username = self.model.normalize_username(username)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         if password is None:
#             raise TypeError('Password should not be none')

#         user = self.create_user(email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()
#         return user



# class User(AbstractBaseUser, PermissionsMixin):
#     # username = models.CharField(max_length=255, unique=True, db_index=True)
#     name=models.CharField(max_length=50,blank=True, null=True)
#     email = models.EmailField(max_length=255, unique=True, db_index=True)
#     mobile=models.PositiveIntegerField(blank=True, null=True)
#     Otheruser_type = (
#         ("CA", "CA"),
#         ("Accountant", "Accountant"),
#     )
#     type = models.CharField(max_length=20, choices=Otheruser_type,null=True,blank=True)
#     is_verified = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=True)
#     is_delete = models.BooleanField(null=True)
#     is_edit = models.BooleanField(null=True)
#     is_views = models.BooleanField(null=True)
#     # groups = models.ForeignKey(Group,blank=True,null=True,on_delete=models.DO_NOTHING)
#     created_by=models.CharField(max_length=60)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     # auth_provider = models.CharField(
#     #     max_length=255, blank=False,
#     #     null=False, default=AUTH_PROVIDERS.get('email'))

#     USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = ['username']

#     # REQUIRED_FIELDS = ['email']
#     objects=UserManager()
#     def __str__(self):
#         return self.email
#     def tokens(self):
#         refresh = RefreshToken.for_user(self)
#         return {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token)
#         }    

# class BalancesheetData(models.Model):
#     sheet = models.FileField(upload_to='balancesheet/')
#     profitloss = models.FileField(upload_to='profit&loss/')
#     trialbalance = models.FileField(upload_to='trialbalance/')
#     created_by = models.CharField(max_length=60,null=True,blank=True)


#     def __str__(self):
#         return self.created_by

# class masterBank(models.Model):
#     mstbnk_id = models.AutoField(primary_key=True)
#     mstbnk_nm = models.CharField(max_length=50, blank=True, null=True)
#     actv_flg = models.CharField(max_length=1)
#     entr_by = models.IntegerField(blank=True, null=True)
#     entr_dt = models.DateTimeField(blank=True, null=True)
#     ip_addr = models.CharField(max_length=16, blank=True, null=True)
#     mac_addr = models.CharField(max_length=16, blank=True, null=True)
#     def __str__(self):
#         return self.mstbnk_nm
      

# class PpOrgnM(models.Model):
#     orgn_id = models.AutoField(primary_key=True)
#     usr = models.ForeignKey(User, models.CASCADE)
#     # bankname = models.ForeignKey(PpBnkM,models.CASCADE)
#     orgn_nm = models.ForeignKey(companydata,on_delete=CASCADE,null=True,blank=True)
#     orgn_email = models.CharField(max_length=320, blank=True, null=True)
#     orgn_mobile = models.PositiveIntegerField(blank=True, null=True)
#     orgn_address=models.TextField(blank=True,null=True)
#     orgn_website=models.CharField(max_length=100,blank=True,null=True)
#     orgn_state = models.CharField(max_length=40, blank=True, null=True)
#     orgn_gstin = models.CharField(max_length=40, blank=True, null=True)
#     vat_no=models.CharField(max_length=100,null=True,blank=True)
#     cst_no=models.CharField(max_length=100,null=True,blank=True)
#     pan_no=models.CharField(max_length=100,null=True,blank=True)
#     orgn_ex_nm = models.CharField(max_length=50, blank=True, null=True)
#     actv_flg = models.CharField(max_length=1)
#     entr_by = models.CharField(blank=True, null=True,max_length=50)
#     entr_dt = models.DateTimeField(blank=True, null=True)
#     ip_addr = models.CharField(max_length=16, blank=True, null=True)
#     mac_addr = models.CharField(max_length=16, blank=True, null=True)

#     def __str__(self):
#         return str(self.orgn_nm)

#     @property
#     def bnklist(self):
#         return self.ppbnkm_set.all()         

# class PpBnkM(models.Model):
#         # reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
#     bnk_id = models.AutoField(primary_key=True)
#     usr = models.ForeignKey(User, on_delete=models.CASCADE)
#     masterbank_id = models.ForeignKey(masterBank, on_delete=models.CASCADE)
#     ifsc_code=models.CharField(max_length=100,null=True,blank=True)
#     account_no=models.CharField(max_length=100,null=True,blank=True)
#     orgn_id = models.ForeignKey(PpOrgnM, on_delete=models.CASCADE)
#     # ladger_name=models.ForeignKey(ladgernamedata,on_delete=CASCADE,null=True,blank=True)
#     bnk_msg_type = models.CharField(max_length=5, blank=True, null=True)
#     bnk_msg_to = models.CharField(max_length=320, blank=True, null=True)
#     bnk_msg_frmt = models.CharField(max_length=1000, blank=True, null=True)
#     actv_flg = models.CharField(max_length=1)
#     cover = models.ImageField(upload_to='images/',blank=True, null=True)
#     entr_by = models.CharField(blank=True, null=True,max_length=50)
#     entr_dt = models.DateTimeField(blank=True, null=True)
#     ip_addr = models.CharField(max_length=16, blank=True, null=True)
#     mac_addr = models.CharField(max_length=16, blank=True, null=True)

#     def __str__(self):
#         return '{0}'.format(self.masterbank_id)

#     # def __str__(self):
#     #     return self.masterbank_id

      

# class PpPayeeM(models.Model):
#     payee_id = models.AutoField(primary_key=True)
#     usr = models.ForeignKey(User,models.DO_NOTHING)
#     payee_nm = models.CharField(max_length=35)
#     payee_ac_no = models.CharField(max_length=25)
#     ex_flg = models.CharField(max_length=1, blank=True, null=True)
#     ex_masterid = models.CharField(max_length=6, blank=True, null=True)
#     ex_vchr_typ = models.CharField(max_length=30, blank=True, null=True)
#     entr_by = models.CharField(blank=True, null=True,max_length=50)
#     entr_dt = models.DateTimeField(blank=True, null=True)
#     ip_addr = models.CharField(max_length=16, blank=True, null=True)
#     mac_addr = models.CharField(max_length=16, blank=True, null=True)

# class Filleupload(models.Model):
#   filedata = models.FileField(upload_to='images/')
#   cordinate=models.IntegerField()

#   def save(self, *args, **kwargs):
#     self.cordinate += 1
#     return super(Filleupload, self).save(*args, **kwargs) #


# class PpLogT(models.Model):
#     log_id = models.AutoField(primary_key=True)
#     usr = models.ForeignKey(User, models.CASCADE)
#     log_tbl = models.CharField(max_length=20, blank=True, null=True)
#     menu_id = models.IntegerField()
#     log_type = models.CharField(max_length=8)
#     log_desc = models.CharField(max_length=200, blank=True, null=True)
#     entr_by = models.IntegerField(blank=True, null=True)
#     entr_dt = models.DateTimeField(blank=True, null=True)
#     ip_addr = models.CharField(max_length=16, blank=True, null=True)
#     mac_addr = models.CharField(max_length=16, blank=True, null=True)



# class PpPymntT(models.Model):
#     pymnt_id = models.AutoField(primary_key=True)
#     bnk_id = models.ForeignKey(PpBnkM,on_delete=models.CASCADE)
#     orgn = models.ForeignKey(PpOrgnM,models.DO_NOTHING)
#     usr = models.ForeignKey(User,models.CASCADE)
#     narration= models.CharField(max_length=100,default=False)
#     demo_test=models.CharField(max_length=30)
#     pymnt_nm = models.ForeignKey(ladgernamedata,on_delete=CASCADE,null=True,blank=True)
#     pymnt_ac_no = models.CharField(max_length=25)
#     pymnt_chq_dt = models.DateField()
#     pymnt_chq_no = models.CharField(max_length=20,blank=True, null=True)
#     pymnt_chq_amt = models.DecimalField(max_digits=15, decimal_places=2)
#     FLAG_TYPE = ( 
#     ("PP", "Print Pending"),
#     ("VP", "Verification Pending"),
#     ("SP", "Sent Pending"),
#     ("CM", "Complete"),
#     ("VC","varified"),
#     ) 
#     pymnt_sts = models.CharField(max_length=30, blank=True, null=True,choices=FLAG_TYPE)
#     paymentactive_status=models.BooleanField(default=0)
#     NUMBER_CHOICES = (
#     ("0","0"),
#     ("1", "1"),
#     ("2", "2"),
#     ("3", "3"),
#     ("4", "4"),
#     ("5", "5"),
#     ("6", "6"),
#     ("7", "7"),
#     ("8", "8"),
#     ("9","9"),
#     ("10","9"),
#     ("11","11"),
#     ("12","12"),
#     )
#     select_month = models.CharField(max_length=12, blank=True, null=True,choices=NUMBER_CHOICES,default=0)
    
#     PYMNT_CHQ_MICR=models.CharField(max_length=15,blank=True, null=True)
#     PYMNT_CHQ_ACCID=models.CharField(max_length=10,blank=True, null=True)
#     PYMNT_CHQ_TRNSID=models.CharField(max_length=4,blank=True, null=True)
#     PYMENT_CHQ_NO=models.CharField(max_length=20,blank=True, null=True)
#     priented_imag=models.ImageField(upload_to='printedimage/')
    
#     ex_flg = models.CharField(max_length=1, blank=True, null=True)
#     ex_masterid = models.CharField(max_length=6, blank=True, null=True)
#     ex_vchr_typ = models.CharField(max_length=30, blank=True, null=True)
#     entr_by = models.CharField(blank=True, null=True,max_length=50)
#     entr_dt = models.DateTimeField(blank=True, null=True)
#     ip_addr = models.CharField(max_length=16, blank=True, null=True)
#     mac_addr = models.CharField(max_length=16, blank=True, null=True)

#     # def save(self, *args, **kwargs):
#     #     if self.priented_imag:
#     #         self.priented_imag = get_thumbnail(self.priented_imag, '2400x1100', quality=300, format = 'JPEG' if ext.lower() == 'jpg' else ext.upper())
#     #     super(PpPymntT, self).save(*args, **kwargs)

#     def __str__(self):
#         return '{0}'.format(self.pymnt_nm)


# class pp_bankcrd_m(models.Model):
#     label=models.CharField(max_length=100)
#     path_img_nm1= models.ImageField(upload_to='temparery/',null=True,blank=True)
#     mstbnk_id=models.CharField(max_length=30, blank=True, null=True)
#     x1=models.IntegerField(blank=True, null=True)
#     y1=models.IntegerField(blank=True, null=True)
#     x2=models.IntegerField(blank=True, null=True)
#     y2=models.IntegerField(blank=True, null=True)

#     payee=models.CharField(max_length=100,blank=True, null=True)
#     x1_payee=models.IntegerField(blank=True, null=True)
#     y1_payee=models.IntegerField(blank=True, null=True)
#     x2_payee=models.IntegerField(blank=True, null=True)
#     y2_payee=models.IntegerField(blank=True, null=True)

#     rupee_w1=models.CharField(max_length=100,blank=True, null=True)    
#     x1_rupee_w1=models.IntegerField(blank=True, null=True)
#     y1_rupee_w1=models.IntegerField(blank=True, null=True)
#     x2_rupee_w1=models.IntegerField(blank=True, null=True)
#     y2_rupee_w1=models.IntegerField(blank=True, null=True)

    
#     rupee_w2=models.CharField(max_length=100,blank=True, null=True)
#     x1_rupee_w2=models.IntegerField(blank=True, null=True)
#     y1_rupee_w2=models.IntegerField(blank=True, null=True)
#     x2_rupee_w2=models.IntegerField(blank=True, null=True)
#     y2_rupee_w2=models.IntegerField(blank=True, null=True)
#     rupee_n=models.CharField(max_length=100,blank=True, null=True)
#     x1_rupee_n=models.IntegerField(blank=True, null=True)
#     y1_rupee_n=models.IntegerField(blank=True, null=True)
#     x2_rupee_n=models.IntegerField(blank=True, null=True)
#     y2_rupee_n=models.IntegerField(blank=True, null=True)
#     date=models.CharField(max_length=100,blank=True, null=True)
#     x1_date=models.IntegerField(blank=True, null=True)
#     y1_date=models.IntegerField(blank=True, null=True)
#     x2_date=models.IntegerField(blank=True, null=True)
#     y2_date=models.IntegerField(blank=True, null=True)

#     entr_by = models.IntegerField(blank=True, null=True)
    


# class pp_path_m(models.Model):
#     path_id=models.AutoField(primary_key=True) 
#     # masterbank_id = models.ForeignKey(PpBnkM, on_delete=models.CASCADE)
#     path_img_nm= models.ImageField(upload_to='blankImg/')


# class term_condition(models.Model):
#     descreption=models.TextField(max_length=2000)
#     is_activate=models.BooleanField()
#     created_by=models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)
#     ip_addr = models.CharField(max_length=16, blank=True, null=True)
#     mac_addr = models.CharField(max_length=16, blank=True, null=True)

   


