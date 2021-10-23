from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.enums import Choices
# from e_checkapp.models import PpOrgnM,PpBnkM, masterBank
from tallyapp.models import companydata
# Create your models here.
    
class masterBank(models.Model):
    mstbnk_nm = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.mstbnk_nm

class BankDetails(models.Model):
    comp_name=models.ForeignKey(companydata,on_delete=models.CASCADE,null=True,blank=True)
    bankname=models.ForeignKey(masterBank,on_delete=models.CASCADE,null=True,blank=True)
    ifsc_code=models.CharField(max_length=100,null=True,blank=True)
    account_no=models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return str(self.bankname)
    
    @property
    def epaymententry(self):
        return self.epaymentdetails_set.all()

class EpaymentDetails(models.Model):
    bankname=models.ForeignKey(BankDetails,on_delete=models.CASCADE,null=True,blank=True)
    file=models.FileField(upload_to='raw',null=True)
    created_on=models.DateField(auto_now_add=True,null=True,blank=True)
    s_date=models.DateField(null=True,blank=True)
    e_date=models.DateField(null=True,blank=True)
    entry=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.bankname)
    
    @property
    def showdataentry(self):
        return self.showdata_set.all()

class LedgerData(models.Model):
    legdername=models.CharField(max_length=30)
    companyname=models.CharField(max_length=30)

    def __str__(self):
        return str(self.legdername)

Choices={('CONTRA VOUCHER','CONTRA VOUCHER'),
            ('PURCHASE VOUCHER','PURCHASE VOUCHER'),('RECEIPT VOUCHER','RECEIPT VOUCHER'),('JOURNAL VOUCHER','JOURNAL VOUCHER'),
            ('SALES VOUCHER','SALES VOUCHER'),('PAYMENT VOUCHER','PAYMENT VOUCHER'),('CREDIT NOTE VOUCHER','CREDIT NOTE VOUCHER'),
            ('DEBIT NOTE VOUCHER','DEBIT NOTE VOUCHER')
}

class ShowData(models.Model):
    bank=models.ForeignKey(EpaymentDetails,on_delete=DO_NOTHING,null=True,blank=True)
    Date=models.DateField(null=True,blank=True)
    Transaction=models.TextField(null=True,blank=True)
    Legder=models.CharField(max_length=200,null=True,blank=True)
    Ref_no=models.CharField(max_length=100,null=True,blank=True)
    AccountantNarration=models.CharField(max_length=500,null=True,blank=True)
    Credit=models.DecimalField(max_digits=15,null=True,blank=True,decimal_places=2)
    Debit=models.DecimalField(max_digits=15,null=True,blank=True,decimal_places=2)
    EditLegder=models.CharField(max_length=200,null=True,blank=True)
    EditLegder2=models.CharField(max_length=200,null=True,blank=True)
    EditLegderamount=models.DecimalField(max_digits=15,null=True,blank=True,decimal_places=2)
    EditLegder2amount=models.DecimalField(max_digits=15,null=True,blank=True,decimal_places=2)
    ListLegder1=models.CharField(max_length=200,null=True,blank=True)
    ListAmount1=models.CharField(max_length=200,null=True,blank=True)
    ListLegder2=models.CharField(max_length=200,null=True,blank=True)
    ListAmount2=models.CharField(max_length=200,null=True,blank=True)
    Vouchetype=models.CharField(choices=Choices,max_length=100,null=True,blank=True)
    is_verified=models.BooleanField(null=True,blank=True,default=False)

    def __str__(self):
        return str(self.Transaction)
