from django.contrib import admin
from .models import EpaymentDetails,LedgerData, ShowData,BankDetails,masterBank
# Register your models here.

admin.site.register(EpaymentDetails)
admin.site.register(LedgerData)
admin.site.register(ShowData)
admin.site.register(BankDetails)
admin.site.register(masterBank)