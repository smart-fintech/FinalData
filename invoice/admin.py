from django.contrib import admin
from .models import BuyerData,SellerData,InvoiceData,Invoice,CSVInvoiceData,Uploadcsv,CSVTableData,VoucherInvoiceEntry

# Register your models here.
admin.site.register(BuyerData)
admin.site.register(SellerData)
admin.site.register(Invoice)
admin.site.register(InvoiceData)
admin.site.register(CSVInvoiceData)
admin.site.register(Uploadcsv)
admin.site.register(CSVTableData)
admin.site.register(VoucherInvoiceEntry)