from django.db.models import fields
from rest_framework import serializers
from .models import BuyerData,SellerData,Invoice,InvoiceData,CSVInvoiceData, Uploadcsv,CSvTableData,VoucherInvoiceEntry
from tallyapp.models import companydata,ladgernamedata


class ladgernamedataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ladgernamedata
        fields = '__all__'
class companydataSerializer(serializers.ModelSerializer):
    class Meta:
        model = companydata
        fields = '__all__'

class Uploadcsvserializer1(serializers.ModelSerializer):
    class Meta:
        model=Uploadcsv
        fields = ['Hsn_code','Description','CGst_rate','SGst_rate','IGst_rate','Per','Rate']

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerData
        fields = ['id','buyer_company', 'buyer_name',
                  'buyer_phone', 'buyer_email', 'buyer_address', 'buyer_state', 'buyer_gstin','buyer_website']
    def to_representation(self, instance):
        data = super(BuyerSerializer, self).to_representation(instance)
        data['buyer_company'] = instance.buyer_company.ledeger_name
        return data


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerData
        fields = ['id','seller_company', 'seller_name',
                  'seller_phone', 'seller_email', 'seller_address', 'seller_website', 'seller_state', 'seller_gstin']
    def to_representation(self, instance):
        rep = super(SellerSerializer, self).to_representation(instance)
        rep['seller_company'] = instance.seller_company.comp_name
        return rep
class InvoiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceData
        fields='__all__'
        # fields = ['Invoice_data', 'Products', 'HSN_details','quantity']
    def to_representation(self, instance):
        rep = super(InvoiceDataSerializer, self).to_representation(instance)
        rep['Invoice_data'] = instance.Invoice_data.Invoice_no
        return rep
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id','Seller_data', 'Buyer_data','Invoice_no', 'Invoice_date', 'P_O_no', 'P_O_date', 'Terms_of_payment', 'Reference_no','Total',
                  'Delievry_note','Roundoff','GSTTotal']
    def to_representation(self, instance):
        data = super(InvoiceSerializer, self).to_representation(instance)
        data['Buyer_data'] = instance.Buyer_data.buyer_company.ledeger_name
        data['Seller_data'] = instance.Seller_data.seller_company.comp_name
        return data


class InvoiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceData
        fields='__all__'
        # fields = ['Invoice_data', 'Products', 'HSN_details','quantity']
    def to_representation(self, instance):
        rep = super(InvoiceDataSerializer, self).to_representation(instance)
        rep['Invoice_data'] = instance.Invoice_data.Invoice_no
        return rep
class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = CSVInvoiceData
        fields = ('file','Company')
class CSVTableData(serializers.ModelSerializer):
    class Meta:
        model = CSvTableData
        fields='__all__'
class Getcsvinvoicedata(serializers.ModelSerializer):
    csvreceipt=CSVTableData(read_only=True,many=True)
    class Meta:
        model = CSVInvoiceData
        fields = ['id','companyname','file','invoice_no','subtotal','invoice_date','payment_mode','CGST','SGST','IGST','bank_details','company_details','csvreceipt']
    def create(self, validated_data):
        return CSVInvoiceData.objects.create(**validated_data)

class AnotherMainSerializer(serializers.ModelSerializer):
    invoicedatas=InvoiceDataSerializer(read_only=True,many=True)
    class Meta:
        model=Invoice
        fields=['id','Invoice_no','Buyer_data','Seller_data','Total','Invoice_date','P_O_no','P_O_date','Terms_of_payment','Reference_no','Delievry_note','file','invoicedatas']

class MainInvoice(serializers.ModelSerializer):
    buyerinvoice=AnotherMainSerializer(read_only=True,many=True)
    class Meta:
        model=BuyerData
        fields=['id','buyer_company', 'buyer_name',
                  'buyer_phone', 'buyer_email', 'buyer_address', 'buyer_state', 'buyer_gstin','buyerinvoice']

class AnotherMainSerializer(serializers.ModelSerializer):
    invoicedatas=InvoiceDataSerializer(read_only=True,many=True)
    class Meta:
        model=Invoice
        fields=['id','Invoice_no','Buyer_data','Seller_data','Total','Invoice_date','P_O_no','P_O_date','Terms_of_payment','Reference_no','Delievry_note','file','invoicedatas']
class CSVTableData1(serializers.ModelSerializer):
    class Meta:
        model = CSvTableData
        fields='__all__'

class ReciptReportSerializer(serializers.ModelSerializer):
    csvreceipt=CSVTableData1(read_only=True,many=True)
    

    class Meta:
        model=CSVInvoiceData
        fields = ['id','file','companyname','Company','invoice_no','subtotal','invoice_date','payment_mode','CGST','SGST','IGST','bank_details','company_details','csvreceipt']

class CreateReportSerializer(serializers.ModelSerializer):
    invoicedatas=InvoiceDataSerializer(read_only=True,many=True)

    class Meta:
        model=Invoice
        fields = ['id','Buyer_data','Seller_data','Invoice_no','Invoice_date','P_O_no','P_O_date','Total','Terms_of_payment','Reference_no','Delievry_note','file','invoicedatas']
    def to_representation(self, instance):
        rep = super(CreateReportSerializer, self).to_representation(instance)
        rep['Buyer_data'] = instance.Buyer_data.buyer_company.companyname
        return rep
class VoucherInvoiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherInvoiceEntry
        fields='__all__'
    # def to_representation(self, instance):
    #     rep = super(VoucherInvoiceDataSerializer, self).to_representation(instance)
    #     rep['company'] = instance.company.comp_name
    #     return rep


class OtherInsurancedata(serializers.ModelSerializer):
    class Meta:
        model=Invoice
        fields=['id','Packageing','Insurance','Frieght','Others','CGSTPackageing',
    'CGSTInsurance',
    'CGSTFrieght',
    'CGSTOthers',
    'SGSTPackageing',
    'SGSTInsurance',
    'SGSTFrieght',
    'SGSTOthers',
    'IGSTPackageing',
    'IGSTInsurance',
    'IGSTFrieght',
    'IGSTOthers',]
