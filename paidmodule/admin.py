from django.contrib import admin
from e_checkapp.models import PpBnkM,PpOrgnM,User,PpPymntT
from .models import clonedata,sailary


# Register your models here.
admin.site.register(clonedata)
admin.site.register(sailary)