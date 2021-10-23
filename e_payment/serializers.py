from rest_framework import serializers
from tallyapp.models import ladgernamedata,companydata
from tallyapp.serializers import *
from .models import EpaymentDetails, ShowData,BankDetails,masterBank

class masterBankSerializer(serializers.ModelSerializer):
    class Meta:
        model=masterBank
        fields='__all__'

class BankDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=BankDetails
        # fields='__all__'
        fields=['id','comp_name','bankname','ifsc_code','account_no']

    def to_representation(self, instance):
        data = super(BankDataSerializer, self).to_representation(instance)
        data['bankname'] = instance.bankname.mstbnk_nm
        return data

class ShowBankDataSerializer(serializers.ModelSerializer):   
    class Meta:
        model=BankDetails
        # fields='__all__'
        fields=['id','comp_name','bankname','ifsc_code','account_no']
    def to_representation(self, instance):
        rep = super(ShowBankDataSerializer, self).to_representation(instance)
        rep['comp_name'] = instance.comp_name.comp_name
        rep['bankname'] = instance.bankname.mstbnk_nm
        return rep

class EpaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=EpaymentDetails
        fields=['bankname','file']
    
    def to_representation(self, instance):
        data = super(EpaymentSerializer, self).to_representation(instance)
        data['bankname'] = instance.bankname.bankname.mstbnk_nm
        return data
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bankname'].queryset = BankDetails.objects.all()

class ShowDataSerializer(serializers.ModelSerializer):
    ListAmount1 = serializers.ListField(child = serializers.CharField(max_length=200,allow_null=True,default=None,required=False))
    ListLegder1 = serializers.ListField(child = serializers.CharField(max_length=200,allow_null =True,default=None,required=False))
    ListAmount2 = serializers.ListField(child = serializers.CharField(max_length=200,allow_null =True,default=None,required=False))
    ListLegder2 = serializers.ListField(child = serializers.CharField(max_length=200,allow_null=True,default=None,required=False))
    class Meta:
        model=ShowData
        fields='__all__'

    def to_representation(self, instance):
        data = super(ShowDataSerializer, self).to_representation(instance)
        data['bank'] = instance.bank.bankname.bankname.mstbnk_nm
        return data
    

class EpaymentSerializer1(serializers.ModelSerializer):
    showdataentry=ShowDataSerializer(many=True,read_only=True)

    class Meta:
        model=EpaymentDetails
        fields=['id','bankname','file','created_on','e_date','s_date','showdataentry','entry']
    
    def to_representation(self, instance):
        data = super(EpaymentSerializer1, self).to_representation(instance)
        data['bankname'] = instance.bankname.bankname.mstbnk_nm
        return data

class LedgerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=ladgernamedata
        fields=['id','ledeger_name']
class LedgerDataSerializer1(serializers.ModelSerializer):
    class Meta:
        model=ladgernamedata
        fields= ['id','ledeger_name','ledeger_email', 'ledeger_phone', 'ledeger_address',
        'ledeger_state','ledeger_website','ledeger_gstin']

class UpdateBankDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=BankDetails
        # fields='__all__'
        fields=['id','comp_name','bankname','ifsc_code','account_no']

    def to_representation(self, instance):
        data = super(UpdateBankDataSerializer, self).to_representation(instance)
        data['comp_name'] = instance.comp_name.comp_name
        data['bankname'] = instance.bankname.mstbnk_nm
        return data
