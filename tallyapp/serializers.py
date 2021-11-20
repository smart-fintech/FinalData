from rest_framework import serializers
from tallyapp.models import ladgernamedata, companydata,voucherfromtally


class ladegerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ladgernamedata
        fields = ['id', 'name']

class PostladegerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ladgernamedata
        fields = ['ledeger_name']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = companydata
        fields = ['id','comp_name','comp_id']   

class NormalCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = companydata
        fields = ['id','comp_name','comp_email', 'comp_phone', 'comp_address',
        'comp_state','comp_website','comp_gstin','mac_ad','vat_no','cst_no','pan_no',]

class UpdateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = companydata
        fields = ['id','comp_name','comp_email', 'comp_phone', 'comp_address',
        'comp_state','comp_website','comp_gstin','mac_ad','vat_no','cst_no','pan_no',]        

class UpdateLegderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ladgernamedata
        fields = ['id','ledeger_name','ledeger_email', 'ledeger_phone', 'ledeger_address',
        'ledeger_state','ledeger_website','ledeger_gstin']
class GetvoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = voucherfromtally
        fields = ['Legder','OppositeLegder','Date','Credit','Debit','Vouchetype']
