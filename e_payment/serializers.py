
from rest_framework import serializers

from tallyapp.models import ladgernamedata,companydata
from .models import EpaymentDetails, ShowData,BankDetails,masterBank
# from e_checkapp.models import PpOrgnM,PpBnkM


class masterBankSerializer(serializers.ModelSerializer):
    class Meta:
        model=masterBank
        fields='__all__'

class BankDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=BankDetails
        # fields='__all__'
        fields=['id','companyname','bankname','ifsc_code','account_no']

    def to_representation(self, instance):
        data = super(BankDataSerializer, self).to_representation(instance)
        data['companyname'] = instance.companyname.comp_name
        data['bankname'] = instance.bankname.mstbnk_nm
        return data

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
        fields='__all__'



