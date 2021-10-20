import io
import csv
from django.db import models
from django.conf import settings
from django.http.response import Http404
from pandas.io.parsers import read_csv
from tallyapp.models import companydata,ladgernamedata
from django.db.models import manager, query
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.views import APIView
from .models import BuyerData,SellerData,InvoiceData,Invoice,CSVInvoiceData,Uploadcsv,VoucherInvoiceEntry,CSvTableData
from .serializers import AnotherMainSerializer,VoucherInvoiceDataSerializer,OtherInsurancedata, MainInvoice,ReciptReportSerializer, CreateReportSerializer,BuyerSerializer,companydataSerializer,SellerSerializer,Uploadcsvserializer1,InvoiceSerializer,InvoiceDataSerializer,Getcsvinvoicedata,FileUploadSerializer,MainInvoice,ladgernamedataSerializer
from rest_framework import generics, serializers,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
import pandas as pd
import pandas as pd
import os,re,camelot
import datetime
# import camelot
import requests
from invoice.MLcode.detect import latestcode
from pdf2image import convert_from_path

class ReceiptReportViews(APIView):
    def get(self,request):
        queryset=CSVInvoiceData.objects.all()
        print(queryset)
        serializer = ReciptReportSerializer(queryset, many=True)
        return Response(serializer.data)
class CompanyShow(APIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = companydataSerializer

    def get(self, request, format=None):
        loging_user=request.user
        snippets =companydata.objects.all()
        print("Sssssssssss",snippets)
        serializer = companydataSerializer(snippets, many=True)
        return Response(serializer.data)  
class LegderShow(APIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = ladgernamedataSerializer
    def get(self, request, format=None):
        loging_user=request.user
        snippets =ladgernamedata.objects.all()
        serializer = ladgernamedataSerializer(snippets, many=True)
        return Response(serializer.data)  


class UploadCSVView(generics.CreateAPIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = Uploadcsvserializer1

    def post(self, request, *args, **kwargs):
        login_user=request.user
        serializer_class = self.get_serializer(data=request.data)
        serializer_class.is_valid()
        serializer_class.save(user=login_user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get(self, request, *args, **kwargs):
        query= Uploadcsv.objects.all()
        serializer=Uploadcsvserializer1(query,many=True)
        return Response(serializer.data)
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
 class UpdateHsndetails(APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Uploadcsv.objects.get(pk=pk)
        except Uploadcsv.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = Uploadcsvserializer1(snippet)
        return Response(serializer.data)
    
    def patch(self, request,pk, *args, **kwargs):
        snippet = self.get_object(pk)
        serializer = Uploadcsvserializer1(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class NewMainInvoiceShow(APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = MainInvoice
    def get(self,request,*args,**kwargs):
        query= BuyerData.objects.all()
        serializer=MainInvoice(query,many=True)
        return Response(serializer.data)
class MainInvoiceShow(APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class =AnotherMainSerializer
    def get(self,request,*args,**kwargs):
        queryset= Invoice.objects.all()
        serializer=AnotherMainSerializer(queryset,many=True)
        print(serializer.data)
        return Response(serializer.data)


class BuyerDetailsView(APIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = BuyerSerializer

    def post(self, request, format=None):
        serializer = BuyerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self,request,*args,**kwargs):
    #     loginuser=request.user
    #     query= BuyerData.objects.filter(created_by=loginuser).order_by('-id')[0]
    #     serializer=BuyerSerializer(query)
    #     return Response(serializer.data)

    
class Buyerdataeditdelete(APIView):
    """
    Retrieve, update or delete a org instance.
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = BuyerSerializer
    def get_object(self, pk):
        try:
            return BuyerData.objects.get(pk=pk)
        except BuyerData.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = BuyerSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = BuyerSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class SellerDetailsView(APIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = SellerSerializer

    # def get(self,request,*args,**kwargs):
    #     loginuser=request.user
    #     query = SellerData.objects.filter(created_by=loginuser).order_by('-id')[0]
    #     serializer = SellerSerializer(query,many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Sellerdataeditdelete(APIView):
    """
    Retrieve, update or delete a org instance.
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = SellerSerializer
    def get_object(self, pk):
        try:
            return SellerData.objects.get(pk=pk)
        except SellerData.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SellerSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SellerSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class InvoiceDetailsView(APIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = InvoiceSerializer
    def post(self, request, format=None):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Invoicetotal(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self,request):
        inv=Invoice.objects.latest('id')
        serializer = InvoiceSerializer(inv)
        return Response(serializer.data)
    def put(self,request):
        inv=Invoice.objects.latest('id')
        serializer = InvoiceSerializer(inv, data=request.data)
        if serializer.is_valid():
            inv.Total=request.data['Total']
            inv.Roundoff=request.data['Roundoff']
            inv.GSTTotal=request.data['GSTTotal']
            inv.save()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvoiceOtherdata(APIView):
    # permission_classes = (IsAuthenticated,)
    def patch(self,request):
        inv=Invoice.objects.latest('id')
        serializer = OtherInsurancedata(inv, data=request.data)
        if serializer.is_valid():
            inv.Packageing=request.data['Packageing']
            inv.Insurance=request.data['Insurance']
            inv.Frieght=request.data['Frieght']
            inv.Insurance=request.data['Insurance']
            inv.CGSTInsurance=request.data['CGSTInsurance']
            inv.CGSTPackageing=request.data['CGSTPackageing']
            inv.CGSTFrieght=request.data['CGSTFrieght']
            inv.CGSTOthers=request.data['CGSTOthers']
            inv.SGSTPackageing=request.data['SGSTPackageing']
            inv.SGSTInsurance=request.data['SGSTInsurance']
            inv.SGSTFrieght=request.data['SGSTFrieght']
            inv.SGSTOthers=request.data['SGSTOthers']
            inv.IGSTInsurance=request.data['IGSTInsurance']
            inv.IGSTPackageing=request.data['IGSTPackageing']
            inv.IGSTFrieght=request.data['IGSTFrieght']
            inv.IGSTOthers=request.data['IGSTOthers']
            inv.Others=request.data['Others']
            inv.save()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Invoiceeeditdelete(APIView):
    """
    Retrieve, update or delete a org instance.
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = InvoiceSerializer
    def get_object(self, pk):
        try:
            return Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = InvoiceSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            snippet.Total=request.data['Total']
            print(snippet.Total)
            snippet.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InvoiceDataView(APIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)

    serializer_class = InvoiceDataSerializer

    
    def post(self, request, format=None):
        serializer = InvoiceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Invoicedataeeditdelete(APIView):
    """
    Retrieve, update or delete a org instance.
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = InvoiceDataSerializer
    def get_object(self, pk):
        try:
            return InvoiceData.objects.get(pk=pk)
        except InvoiceData.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = InvoiceDataSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = InvoiceDataSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CsvInvoicedataAPI(generics.ListCreateAPIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = FileUploadSerializer
    def post(self, request, *args, **kwargs):
        login_user=request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        value=serializer.data['file']
        print(value)
        images = convert_from_path(str(settings.BASE_DIR)+str(value))
        for i, image in enumerate(images):
            fname = "test1" + ".jpeg"
            path = (str(settings.BASE_DIR)+'/invoice/MLcode/output/')
            image.save(path+ fname) 
            print(path+ fname)
        latestcode()
        df=pd.read_csv(str(settings.BASE_DIR)+'/invoice/MLcode/temp/newocr.csv')
        def convert_nu(text):
            num=re.findall(r'[\d]*[.\d]+',text)
            return "".join(num)
        df['new_sub']=df['sub_total'].apply(lambda x:convert_nu(x))
        df["new_sub"] = pd.to_numeric(df["new_sub"], downcast="float")
        x=df["new_sub"][0]
        y=x.astype(float)
        df.to_csv(settings.MEDIA_ROOT +'/recieveinvoice/new.csv')
        with open(settings.MEDIA_ROOT +'/recieveinvoice/new.csv', 'r') as f:
            reader=csv.DictReader(f)
            for row in reader:
                p= CSVInvoiceData.objects.latest('id')
                p.user=login_user, 
                p.companyname=row.get('company_name',''),
                p.invoice_no=row.get('invoice_number',''),
                # p.subtotal=z,
                p.invoice_date=row.get('invoice_date',''),
                p.payment_mode=row.get('invoice_payment_mode',''),
                p.bank_details=row.get('company_bank_detail',''),
                p.company_details=row.get('company_detail',''),
                p.CGST=row.get('company_tax_detail',''),
                p.SGST=row.get('company_tax_detail',''),
                p.IGST=row.get('company_tax_detail',''),
                model1=companydata.objects.get(id=request.data['Company'])
                p.Company=model1
                p.subtotal=y
                p.save()
        os.remove('media/recieveinvoice/new.csv')
        tables = camelot.read_pdf(str(settings.BASE_DIR)+str(value),pages='all')
        list=['Item Qty','Item Details','HSNCode']
        for i in tables:
            for l in list:
                x=i.df.eq(l).any(axis=0)
                i.to_csv(str(settings.BASE_DIR)+'/media/recieveinvoice/new.csv')
            else:
                pass
            break
        def remove1():
                    x=0
                    with open(str(settings.BASE_DIR)+'/media/recieveinvoice/new.csv', 'r') as f:
                        csv_reader = csv.reader(f)
                        for index,row in enumerate(csv_reader):
                            if 'HSN/SAC' in row:
                                x=index
                                break
                    return x
        diff1=remove1()
        df=pd.read_csv(str(settings.BASE_DIR)+'/media/recieveinvoice/new.csv',header=None)
        t=df.loc[diff1:]
        t.columns=t.iloc[0]
        t=t.reset_index(drop=True)
        t=t[t['HSN/SAC'] != 'HSN/SAC']
        t.dropna(subset = ['HSN/SAC'], inplace=True)
        t.to_csv(str(settings.BASE_DIR)+'/media/recieveinvoice/new.csv')
        with open(str(settings.BASE_DIR)+'/media/recieveinvoice/new.csv', 'r') as f:
            reader=csv.DictReader(f)
            for row in reader:
                model=CSvTableData.objects.create(
                    Products=row.get('Description of Goods',''),
                    HSN_SAC=row.get('HSN/SAC',''),
                    quantity=row.get('Quantity',''),
                    Rate=row.get('Rate',''),
                    Per=row.get('per  Disc. %',''),
                    Discount=row.get('per  Disc. %',''),
                    Amount=row.get('Amount',''),
                )
                model.save()
                query = CSVInvoiceData.objects.get(id=p)
                model.Invoice_data=query
                model.save()
        os.remove('media/recieveinvoice/new.csv')
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        loginuser=request.user
        query = CSVInvoiceData.objects.latest('id')
        serializer = Getcsvinvoicedata(query)
        return Response(serializer.data)

class UpdatecsvDataAPI(generics.RetrieveUpdateAPIView):
    serializer_class = Getcsvinvoicedata
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return CSVInvoiceData.objects.get(pk=pk)
        except CSVInvoiceData.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = Getcsvinvoicedata(snippet)
        return Response(serializer.data)
    
    def put(self, request,pk, *args, **kwargs):
        snippet = self.get_object(pk)
        serializer = Getcsvinvoicedata(snippet, data=request.data)
        data_to_change = {'companyname': request.data.get("companyname")}
        print(data_to_change['companyname'])
        if serializer.is_valid():
            serializer.save(legdername=data_to_change['companyname'])
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class GetcsvInvoicedataAPI(APIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = Getcsvinvoicedata

    def get(self, request, format=None):
        login_uaer_data=request.user
        snippets = CSVInvoiceData.objects.filter(user=login_uaer_data)
        serializer = Getcsvinvoicedata(snippets, many=True)
        return Response(serializer.data)  
        

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
class ModelFilter(django_filters.FilterSet):
    # permission_classes = (IsAuthenticated,)

    Company = django_filters.ModelChoiceFilter(queryset=companydata.objects.all())
    subtotal=django_filters.RangeFilter()
    invoice_date=django_filters.DateTimeFromToRangeFilter()
    class Meta:
        model = CSVInvoiceData
        fields = ['subtotal']
class ReceiptInvoicefilter(generics.ListAPIView):

    queryset=CSVInvoiceData.objects.all()
    serializer_class=ReciptReportSerializer
    filter_backends1 = (DjangoFilterBackend)
    filterset_fields = ['Company','subtotal','invoice_date']    
    filter_class = ModelFilter

class ModelFilter1(django_filters.FilterSet):
    # permission_classes = (IsAuthenticated,)
    Buyer_data = django_filters.ModelChoiceFilter(queryset=BuyerData.objects.all())
    Total=django_filters.RangeFilter()
    Invoice_date=django_filters.DateTimeFromToRangeFilter()


    class Meta:
        model = Invoice
        fields = ['Buyer_data','Total','Invoice_date']
class CreateInvoicefilter(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)

    queryset=Invoice.objects.all()
    serializer_class=CreateReportSerializer
    filter_backends1 = (DjangoFilterBackend)
    filterset_fields = ['Buyer_data','Total','Invoice_date']    
    filter_class = ModelFilter1

class Voucherentry(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = VoucherInvoiceDataSerializer

    def post(self, request, format=None):
        serializer = VoucherInvoiceDataSerializer(data=request.data)
        if serializer.is_valid():
            d = datetime.datetime.strptime(str(request.data['Voucher_date']), '%Y-%m-%d')
            newdate=datetime.date.strftime(d, "%Y%m%d")
            y=-(float(request.data['Voucher_amount_dr']))
            serializer.save(Voucher_amount_dr=y,is_verified=True)
            # url='http://192.168.29.141:9000'
            data='<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>Import</TALLYREQUEST><TYPE>Data</TYPE><ID>Vouchers</ID></HEADER>'
            data+='<BODY><DESC><STATICVARIABLES><SVCURRENTCOMPANY>'+str(serializer.data['company'])+'</SVCURRENTCOMPANY></STATICVARIABLES></DESC><DATA>'
            data+='<TALLYMESSAGE><VOUCHER><DATE>'+str(newdate)
            data+='</DATE><NARRATION>'+(serializer.data['Narration'])
            data+='</NARRATION><VOUCHERTYPENAME>Payment</VOUCHERTYPENAME>'
            data+='<ALLLEDGERENTRIES.LIST><LEDGERNAME>'+serializer.data['legdername']
            data+='</LEDGERNAME><ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>'
            data+='<AMOUNT>'+str(serializer.data['Voucher_amount_dr'])
            data+='</AMOUNT></ALLLEDGERENTRIES.LIST><ALLLEDGERENTRIES.LIST>'
            data+='<LEDGERNAME>'+str(serializer.data['Voucher_type'])
            data+='</LEDGERNAME><ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>'
            data+='<AMOUNT>'+str(serializer.data['Voucher_amount_cr'])
            data+='</AMOUNT></ALLLEDGERENTRIES.LIST></VOUCHER>'
            data+='</TALLYMESSAGE></DATA></BODY></ENVELOPE>'
            req = requests.post(url=url, data=data)
            if serializer.data['CGSTlegderdata'] and serializer.data['CGSTlegderdataamount']:
                d = datetime.datetime.strptime(str(request.data['Voucher_date']), '%Y-%m-%d')
                newdate=datetime.date.strftime(d, "%Y%m%d")
                t=-(float(request.data['CGSTlegderdataamount']))
                serializer.save(Voucher_amount_dr=y,is_verified=True)
                # url='http://192.168.29.141:9000'
                data='<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>Import</TALLYREQUEST><TYPE>Data</TYPE><ID>Vouchers</ID></HEADER>'
                data+='<BODY><DESC><STATICVARIABLES><SVCURRENTCOMPANY>'+str(serializer.data['company'])+'</SVCURRENTCOMPANY></STATICVARIABLES></DESC><DATA>'
                data+='<TALLYMESSAGE><VOUCHER><DATE>'+str(newdate)
                data+='</DATE><NARRATION>'+(serializer.data['Narration'])
                data+='</NARRATION><VOUCHERTYPENAME>Payment</VOUCHERTYPENAME>'
                data+='<ALLLEDGERENTRIES.LIST><LEDGERNAME>'+serializer.data['CGSTlegderdata']
                data+='</LEDGERNAME><ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>'
                data+='<AMOUNT>'+str(serializer.data['CGSTlegderdataamount'])
                data+='</AMOUNT></ALLLEDGERENTRIES.LIST><ALLLEDGERENTRIES.LIST>'
                data+='<LEDGERNAME>'+str(serializer.data['Voucher_type'])
                data+='</LEDGERNAME><ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>'
                data+='<AMOUNT>'+str(t)
                data+='</AMOUNT></ALLLEDGERENTRIES.LIST></VOUCHER>'
                data+='</TALLYMESSAGE></DATA></BODY></ENVELOPE>'
                req = requests.post(url=url, data=data)
                if serializer.data['SGSTlegderdata'] and serializer.data['SCGSTlegderdataamount']:
                    d = datetime.datetime.strptime(str(request.data['Voucher_date']), '%Y-%m-%d')
                    newdate=datetime.date.strftime(d, "%Y%m%d")
                    x=-(float(request.data['SCGSTlegderdataamount']))
                    # url='http://192.168.29.141:9000'
                    data='<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>Import</TALLYREQUEST><TYPE>Data</TYPE><ID>Vouchers</ID></HEADER>'
                    data+='<BODY><DESC><STATICVARIABLES><SVCURRENTCOMPANY>'+str(serializer.data['company'])+'</SVCURRENTCOMPANY></STATICVARIABLES></DESC><DATA>'
                    data+='<TALLYMESSAGE><VOUCHER><DATE>'+str(newdate)
                    data+='</DATE><NARRATION>'+(serializer.data['Narration'])
                    data+='</NARRATION><VOUCHERTYPENAME>Payment</VOUCHERTYPENAME>'
                    data+='<ALLLEDGERENTRIES.LIST><LEDGERNAME>'+serializer.data['SGSTlegderdata']
                    data+='</LEDGERNAME><ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>'
                    data+='<AMOUNT>'+str(serializer.data['SCGSTlegderdataamount'])
                    data+='</AMOUNT></ALLLEDGERENTRIES.LIST><ALLLEDGERENTRIES.LIST>'
                    data+='<LEDGERNAME>'+str(serializer.data['Voucher_type'])
                    data+='</LEDGERNAME><ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>'
                    data+='<AMOUNT>'+str(x)
                    data+='</AMOUNT></ALLLEDGERENTRIES.LIST></VOUCHER>'
                    data+='</TALLYMESSAGE></DATA></BODY></ENVELOPE>'
                    req = requests.post(url=url, data=data)
            elif serializer.data['IGSTlegderdata'] and serializer.data['IGSTlegderdataamount']:
                d = datetime.datetime.strptime(str(request.data['Voucher_date']), '%Y-%m-%d')
                newdate=datetime.date.strftime(d, "%Y%m%d")
                y=-(float(request.data['IGSTlegderdataamount']))
                # url='http://192.168.29.141:9000'
                data='<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>Import</TALLYREQUEST><TYPE>Data</TYPE><ID>Vouchers</ID></HEADER>'
                data+='<BODY><DESC><STATICVARIABLES><SVCURRENTCOMPANY>'+str(serializer.data['company'])+'</SVCURRENTCOMPANY></STATICVARIABLES></DESC><DATA>'
                data+='<TALLYMESSAGE><VOUCHER><DATE>'+str(newdate)
                data+='</DATE><NARRATION>'+(serializer.data['Narration'])
                data+='</NARRATION><VOUCHERTYPENAME>Payment</VOUCHERTYPENAME>'
                data+='<ALLLEDGERENTRIES.LIST><LEDGERNAME>'+serializer.data['IGSTlegderdata']
                data+='</LEDGERNAME><ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>'
                data+='<AMOUNT>'+str(serializer.data['IGSTlegderdataamount'])
                data+='</AMOUNT></ALLLEDGERENTRIES.LIST><ALLLEDGERENTRIES.LIST>'
                data+='<LEDGERNAME>'+str(serializer.data['Voucher_type'])
                data+='</LEDGERNAME><ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>'
                data+='<AMOUNT>'+str(y)
                data+='</AMOUNT></ALLLEDGERENTRIES.LIST></VOUCHER>'
                data+='</TALLYMESSAGE></DATA></BODY></ENVELOPE>'
                req = requests.post(url=url, data=data)
            else:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








# @api_view(['GET'])
# def getpdf(request):
#     query1= Invoice.objects.get(pk=1)
#     query=InvoiceData.objects.filter(Invoice_data=query1)
#     template = get_template('invoice.html')
#     html = template.render({'query': query,'query1':query1})
#     pdf = pdfkit.from_string(html, False, options={})

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

#     return response 
