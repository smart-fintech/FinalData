from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import CharField
from tallyapp.models import companydata,ladgernamedata
from decimal import Decimal
# Create your models here.




class Uploadcsv(models.Model):
    Hsn_code=models.CharField(max_length=20,null=True,blank=True)
    Description=models.TextField(null=True,blank=True)
    CGst_rate=models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    SGst_rate=models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    IGst_rate=models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    Per=models.CharField(max_length=30,null=True,blank=True)
    Rate=models.CharField(max_length=20,null=True,blank=True)
    user=CharField(max_length=30,null=True,blank=True)



    def __str__(self):
        return self.Hsn_code
    
    @property
    def invoicedatahsn(self):
        return self.invoicedata_set.all()

class SellerData(models.Model):
    seller_company=models.ForeignKey(companydata,on_delete=models.CASCADE)
    seller_name=models.CharField(max_length=40,blank=True,null=True)
    seller_phone = models.CharField(max_length=12, blank=True, null=True)
    seller_email = models.EmailField(blank=True, null=True)
    seller_address=models.TextField(blank=True,null=True)
    seller_website=models.CharField(max_length=100,blank=True,null=True)
    seller_state = models.CharField(max_length=40, blank=True, null=True)
    seller_gstin = models.CharField(max_length=40, blank=True, null=True)
    created_by=models.CharField(max_length=40,null=True,blank=True)

    def __str__(self):
        return self.seller_name
    @property
    def sellerinvoice(self):
        return self.invoice_set.all()

    
class BuyerData(models.Model):
    buyer_company = models.ForeignKey(ladgernamedata, on_delete=models.CASCADE, blank=True, null=True)
    buyer_name = models.CharField(max_length=40, blank=True, null=True)
    buyer_phone = models.CharField(max_length=12, blank=True, null=True)
    buyer_email = models.EmailField(blank=True, null=True)
    buyer_address = models.TextField(blank=True, null=True)
    buyer_website=models.CharField(max_length=100,blank=True,null=True)
    buyer_state = models.CharField(max_length=40, blank=True, null=True)
    buyer_gstin = models.CharField(max_length=40, blank=True, null=True)
    created_by = models.CharField(max_length=40, null=True, blank=True)


    def __str__(self):
        #return self.buyer_name
        return str(self.buyer_company) if self.buyer_company else ''
    @property
    def buyerinvoice(self):
        return self.invoice_set.all()

class Invoice(models.Model):
    Seller_data = models.ForeignKey(SellerData, on_delete=models.CASCADE)
    Buyer_data = models.ForeignKey(BuyerData, on_delete=models.CASCADE)
    Invoice_no = models.CharField(max_length=20, blank=True, null=True)
    Invoice_date = models.DateField(blank=True, null=True)
    P_O_no = models.CharField(max_length=30, blank=True, null=True)
    P_O_date = models.DateField(blank=True, null=True)
    Terms_of_payment = models.CharField(max_length=30, blank=True, null=True)
    Reference_no = models.CharField(max_length=100, blank=True, null=True)
    Delievry_note = models.CharField(max_length=100, blank=True, null=True)
    Total = models.FloatField(max_length=40, null=True, blank=True)
    Packageing=models.IntegerField(null=True, blank=True)
    Insurance=models.IntegerField(null=True, blank=True)
    Frieght=models.IntegerField(null=True, blank=True)
    Others=models.IntegerField(null=True, blank=True)
    CGSTPackageing=models.FloatField(null=True, blank=True)
    CGSTInsurance=models.FloatField(null=True, blank=True)
    CGSTFrieght=models.FloatField(null=True, blank=True)
    CGSTOthers=models.FloatField(null=True, blank=True)
    SGSTPackageing=models.FloatField(null=True, blank=True)
    SGSTInsurance=models.FloatField(null=True, blank=True)
    SGSTFrieght=models.FloatField(null=True, blank=True)
    SGSTOthers=models.FloatField(null=True, blank=True)
    IGSTPackageing=models.FloatField(null=True, blank=True)
    IGSTInsurance=models.FloatField(null=True, blank=True)
    IGSTFrieght=models.FloatField(null=True, blank=True)
    IGSTOthers=models.FloatField(null=True, blank=True)
    Roundoff=models.FloatField(max_length=40, null=True, blank=True)
    GSTTotal=models.FloatField(max_length=40, null=True, blank=True)
    IRN=models.CharField(max_length=200,null=True,blank=True)
    Ack_No=models.CharField(max_length=200,null=True,blank=True)
    Ack_Date=models.CharField(max_length=200,null=True,blank=True)
    created_by = models.CharField(max_length=40, null=True, blank=True)
    

    def __str__(self):
        return self.Invoice_no
    @property
    def invoicedatas(self):
        return self.invoicedata_set.all()


class InvoiceData(models.Model):
    Invoice_data=models.ForeignKey(Invoice,on_delete=models.CASCADE)
    Products = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    HSN_details=models.ForeignKey(Uploadcsv,on_delete=DO_NOTHING,null=True,blank=True)
    Discount=models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    Amount=models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    CGST=models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    SGST = models.DecimalField(max_digits=6,decimal_places=2,null=True, blank=True)
    IGST = models.DecimalField(max_digits=6,decimal_places=2,null=True, blank=True)
    Hsn_code = models.CharField(max_length=20, blank=True, null=True)
    Rate = models.CharField(max_length=20, blank=True, null=True)
    Per = models.CharField(max_length=40, blank=True, null=True)
    created_by = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return str(self.Invoice_data)

class CSVInvoiceData(models.Model):
    Company=models.ForeignKey(companydata,on_delete=models.CASCADE,null=True,blank=True)
    file=models.FileField(upload_to='recieveinvoice/',null=True,blank=True)
    created_by=models.CharField(max_length=30,null=True,blank=True)
    companyname=models.CharField(max_length=80,null=True,blank=True)
    invoice_no=models.CharField(max_length=800,null=True,blank=True)
    subtotal=models.FloatField(max_length=70,null=True,blank=True)
    invoice_date=models.DateField(null=True,blank=True)
    CGST=models.CharField(max_length=700,null=True,blank=True)
    SGST = models.CharField(max_length=700,null=True, blank=True)
    IGST = models.CharField(max_length=700,null=True, blank=True)
    created_on=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    StateCode=models.CharField(max_length=10,null=True, blank=True)
    class Meta:
        unique_together = ('invoice_no','invoice_date')
    # def __str__(self):
    #     return self.invoice_no

    @property
    def csvreceipt(self):
        return self.csvtabledata_set.all()

class CSVTableData(models.Model):
    Invoice_data=models.ForeignKey(CSVInvoiceData,on_delete=models.CASCADE)
    Products = models.TextField(null=True, blank=True)
    HSN_SAC=models.CharField(max_length=20,null=True,blank=True)
    GST_rate=models.CharField(max_length=20,null=True,blank=True)
    quantity = models.CharField(max_length=20,null=True, blank=True)
    Rate=models.CharField(max_length=100,null=True,blank=True)
    Per=models.CharField(max_length=100,null=True,blank=True)
    Discount=models.CharField(max_length=100,null=True,blank=True)
    Amount=models.CharField(max_length=40,null=True,blank=True)
    
    def __str__(self):
        return self.Products


class VoucherInvoiceEntry(models.Model):
    company=models.ForeignKey(companydata,on_delete=models.CASCADE,null=True,blank=True)
    Voucher_date=models.DateField(blank=True,null=True)
    legdername=models.CharField(max_length=50,blank=True,null=True)
    Voucher_amount_cr=models.DecimalField(max_digits=15,null=True,blank=True,decimal_places=2)
    Voucher_amount_dr=models.DecimalField(max_digits=15,null=True,blank=True,decimal_places=2)
    Narration=models.CharField(max_length=50,blank=True,null=True)
    CGSTlegderdata=models.CharField(max_length=50,blank=True,null=True)
    CGSTlegderamount=models.DecimalField(max_digits=15,null=True,blank=True,decimal_places=2)
    SGSTlegderdata=models.CharField(max_length=50,blank=True,null=True)
    SGSTlegderamount=models.DecimalField(max_digits=15,null=True,blank=True,decimal_places=2)
    IGSTlegderdata=models.CharField(max_length=50,blank=True,null=True)
    IGSTlegderamount=models.DecimalField(max_digits=15,null=True,blank=True,decimal_places=2)
    Voucher_type=models.CharField(max_length=100,null=True,blank=True)
    Vouchetype=models.CharField(max_length=100,null=True,blank=True)
    is_verified=models.BooleanField(null=True,blank=True,default=False)
    def __str__(self):
        return self.legdername
    
