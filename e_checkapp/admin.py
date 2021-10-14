from django.contrib import admin
from .models import User,PpBnkM,PpOrgnM,Filleupload,masterBank,PpPymntT,PpLogT,pp_bankcrd_m,pp_path_m,term_condition,BalancesheetData


admin.site.register(User)
admin.site.register(PpBnkM)
admin.site.register(PpOrgnM)
admin.site.register(Filleupload)
admin.site.register(masterBank)
admin.site.register(PpPymntT)
admin.site.register(PpLogT)
admin.site.register(pp_bankcrd_m)
admin.site.register(pp_path_m)
admin.site.register(term_condition)
admin.site.register(BalancesheetData)



