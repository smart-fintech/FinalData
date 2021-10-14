from django.db import models
from e_checkapp.models import PpBnkM,PpOrgnM,User,PpPymntT
from datetime import timedelta as tdelta


# Create your models here.

class clonedata(models.Model):
    pymnt_id = models.AutoField(primary_key=True)
    bnk_id = models.ForeignKey(PpPymntT,on_delete=models.CASCADE)
    payment_datefield=models.CharField(max_length=100)
    
class sailary(models.Model):
    uer=models.ForeignKey('e_checkapp.User',on_delete=models.CASCADE,null=True,blank=True)
    # file=models.FileField()
    # label=models.CharField(max_length=100)
    Name=models.CharField(max_length=100)
    AMOUNT=models.CharField(max_length=100)



