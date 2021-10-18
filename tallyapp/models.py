from django.db import models
from django.db.models.deletion import CASCADE
# from e_checkapp.models import *
# from tallyapp.models import companydata

# Create your models here.

class ladgernamedata(models.Model):
    ledeger_name = models.CharField(max_length=40, blank=True, null=True)
    ledeger_phone = models.CharField(max_length=40, blank=True, null=True)
    ledeger_email=models.EmailField(blank=True, null=True)
    ledeger_name = models.CharField(max_length=40, blank=True, null=True)
    ledeger_address=models.CharField(max_length=600, blank=True, null=True)
    ledeger_state=models.CharField(max_length=400, blank=True, null=True)
    ledeger_website=models.CharField(max_length=400, blank=True, null=True)
    ledeger_gstin=models.CharField(max_length=400, blank=True, null=True)
    created_by= models.CharField(max_length=40, blank=True, null=True)
    def __str__(self):
        return self.ledeger_name

class companydata(models.Model):
    comp_name=models.CharField(max_length=100)
    user_company=models.CharField(max_length=100)
    comp_phone = models.CharField(max_length=40, blank=True, null=True)
    comp_email=models.EmailField(blank=True, null=True)
    comp_name = models.CharField(max_length=40, blank=True, null=True)
    comp_address=models.CharField(max_length=600, blank=True, null=True)
    comp_state=models.CharField(max_length=400, blank=True, null=True)
    comp_website=models.CharField(max_length=400, blank=True, null=True)
    comp_gstin=models.CharField(max_length=400, blank=True, null=True)
    comp_id=models.CharField(max_length=100,null=True,blank=True)
    comp_ip_address=models.CharField(max_length=100,null=True,blank=True)
    mac_ad=models.CharField(max_length=100,null=True,blank=True)
    vat_no=models.CharField(max_length=100,null=True,blank=True)
    cst_no=models.CharField(max_length=100,null=True,blank=True)
    pan_no=models.CharField(max_length=100,null=True,blank=True)
    created_by= models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.comp_name        
