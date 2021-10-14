from rest_framework import serializers
from tallyapp.models import ladgernamedata, companydata


class ladegerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ladgernamedata
        fields = ['id', 'name']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = companydata
        fields = ['id','comp_name']  

class UpdateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = companydata
        fields = ['id','comp_name','comp_email', 'comp_phone', 'comp_address',
        'comp_state','comp_website','comp_gstin','mac_ad','vat_no','cst_no','pan_no',]        