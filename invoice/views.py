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
from .models import BuyerData,SellerData,InvoiceData,Invoice,CSVInvoiceData,Uploadcsv,VoucherInvoiceEntry,CSVTableData
from .serializers import AnotherMainSerializer,VoucherInvoiceDataSerializer,OtherInsurancedata, MainInvoice,ReciptReportSerializer, PaymentVoucherDataSerializer,PaymentVoucherDataSerializer1,CreateReportSerializer,BuyerSerializer,companydataSerializer,SellerSerializer,Uploadcsvserializer1,InvoiceSerializer,InvoiceDataSerializer,Getcsvinvoicedata,FileUploadSerializer,MainInvoice,Uploadcsvserializer,ladgernamedataSerializer
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
from pdf2image import convert_from_path
from word2number import w2n
import typing
from decimal import Decimal

from borb.pdf.document import Document
from borb.pdf.pdf import PDF
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.toolkit.location.location_filter import LocationFilter
from borb.toolkit.text.regular_expression_text_extraction import RegularExpressionTextExtraction, PDFMatch
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction

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
        serializer = Uploadcsvserializer(snippet)
        return Response(serializer.data)
    
    def patch(self, request,pk, *args, **kwargs):
        snippet = self.get_object(pk)
        serializer = Uploadcsvserializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
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
    permission_classes = (IsAuthenticated,)
    serializer_class = FileUploadSerializer
    def post(self, request, *args, **kwargs):
        login_user=request.user
        print(login_user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save(created_by=login_user)
        value=serializer.data['file']
        value1 = str(settings.BASE_DIR)+value
        o: RegularExpressionTextExtraction = RegularExpressionTextExtraction("Buyer")
        p: RegularExpressionTextExtraction = RegularExpressionTextExtraction("Invoice No.")
        q: RegularExpressionTextExtraction = RegularExpressionTextExtraction("Dated")
        z: RegularExpressionTextExtraction = RegularExpressionTextExtraction("SGST")
        s: RegularExpressionTextExtraction = RegularExpressionTextExtraction("CGST")
        t: RegularExpressionTextExtraction = RegularExpressionTextExtraction("IGST")
        c: RegularExpressionTextExtraction = RegularExpressionTextExtraction("words")
        main_dict={}
        main_file=open(value1, "rb")
        legderlist=[]
        mod=ladgernamedata.objects.all()
        for a in mod:
            legderlist.append(a.ledeger_name)
        try:
            if o:
                d = PDF.loads(main_file, [o])
                assert d is not None
                matches: typing.List[PDFMatch] = o.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(50),
                                        data.get_y() - Decimal(-40),
                                        Decimal(200),
                                        Decimal(200))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)
                d = PDF.loads(main_file, [l0])
                assert d is not None
                x=l1.get_text_for_page(0)
                data=''
                for l in legderlist:
                    if l[:4] in x:
                        data=l
                main_dict['Buyer Data']=data
        except:
            pass
        try:
            if p:
                d = PDF.loads(main_file, [p])
                assert d is not None
                matches: typing.List[PDFMatch] =p.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(10),
                                        data.get_y() - Decimal(15),
                                        Decimal(100),
                                        Decimal(25))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])

                assert d is not None
                main_dict['Invoice Number']=l1.get_text_for_page(0)
        except:
            pass
        try:
            if q:
                d = PDF.loads(main_file, [q])
                assert d is not None
                matches: typing.List[PDFMatch] = q.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(10),
                                        data.get_y() - Decimal(15),
                                        Decimal(100),
                                        Decimal(25))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])

                assert d is not None
                main_dict['Invoice Date']=l1.get_text_for_page(0)
        except:
            pass
        try:
            if z:
                d = PDF.loads(main_file, [z])
                assert d is not None
                matches: typing.List[PDFMatch] = z.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(10),
                                    data.get_y() - Decimal(5),
                                    Decimal(400),
                                    Decimal(10))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])

                assert d is not None
            main_dict['SGST']=l1.get_text_for_page(0)
        except:
            pass
        try:
            if s:
                d = PDF.loads(main_file, [s])
                assert d is not None
                matches: typing.List[PDFMatch] =s.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(10),
                                    data.get_y() - Decimal(5),
                                    Decimal(500),
                                    Decimal(10))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])

                assert d is not None
            main_dict['CGST']=l1.get_text_for_page(0)
        except:
            pass
        try:
            if t:
                d = PDF.loads(main_file, [t])
                assert d is not None
                matches: typing.List[PDFMatch] = t.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(10),
                                    data.get_y() - Decimal(5),
                                    Decimal(400),
                                    Decimal(10))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])

                assert d is not None
            main_dict['IGST']=l1.get_text_for_page(0)
        except:
            pass
        try:
            if o:
                d = PDF.loads(main_file, [o])
                assert d is not None
                matches: typing.List[PDFMatch] = o.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(50),
                                    data.get_y() - Decimal(-5),
                                    Decimal(200),
                                    Decimal(300))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])

                assert d is not None
                x=l1.get_text_for_page(0)
                code=re.findall('\s\d{2}\s',x)
            main_dict['Code']=code[0]
        except:
            pass
        try:
            if c:
                d = PDF.loads(main_file, [c])
                assert d is not None
                matches: typing.List[PDFMatch] = c.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(100),
                             data.get_y() - Decimal(20),
                             Decimal(400),
                             Decimal(10))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)
                d = PDF.loads(main_file, [l0])
                assert d is not None
                x=l1.get_text_for_page(0)
                nex_txt=''
                for i,letter in enumerate(x):
                    if i and letter.isupper():
                        nex_txt+=' '
                    nex_txt+=letter
                main_total=w2n.word_to_num(nex_txt)
            main_dict['Total']=main_total
        except:
            pass
        print(main_dict)
        for i,j in main_dict.items():
            for r in (("Invoice No.\n", ""), ("Dated\n", ""),("SGST ", ""),("IGST ", ""),("CGST ", ""),("STATETAX(SGST) ", ""),("CENTRALTAX(CGST) ", ""),("Invoice Number : ", ""), ("Invoice Date : ", ""),("State/UT Code: ", ""),("TOTAL: ","")):
                j = str(j).replace(*r)
            main_dict.update({i:j})
        date_list=['%d-%m-%y','%d-%m-%Y','%d/%m/%y','%d/%m/%Y','%d-%b-%Y','%d-%B-%Y','%d-%b-%y','%d-%B-%y','%d/%b/%Y','%d/%B/%Y','%d/%b/%y','%d/%B/%y','%d %b %Y','%d.%m.%Y']
        
        for i in date_list:
            try:
                main_date=datetime.datetime.strptime(main_dict['Invoice Date'], i).date()
            except:
                pass
        inv=CSVInvoiceData.objects.latest('id')
        inv.companyname=main_dict['Buyer Data']
        inv.invoice_no=main_dict['Invoice Number']
        inv.invoice_date=main_date
        igst: RegularExpressionTextExtraction = RegularExpressionTextExtraction("IGST")
        gst=''
        try:
            if igst:
                d = PDF.loads(main_file, [igst])
                assert d is not None
                matches: typing.List[PDFMatch] = igst.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(10),
                             data.get_y() - Decimal(10),
                             Decimal(80),
                             Decimal(20))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])

                assert d is not None
                gst=l1.get_text_for_page(0)
        except:
            pass
        if 'CGST' in main_dict.keys():
            print('cgst,sgst')
            inv.CGST=main_dict['CGST']
            inv.SGST=main_dict['SGST']
        elif 'IGST' in main_dict.keys():
            inv.IGST=main_dict['IGST']
        else:
            pass
        inv.StateCode=main_dict['Code']
        model1=companydata.objects.get(id=request.data['Company'])
        inv.Company=model1
        if 'Total' in main_dict.keys():
            inv.subtotal=main_dict['Total']
        else:
            pass
        inv.save()
        # name_of_file=str(settings.BASE_DIR)+'/media/tabula/tabula-Accounting Voucher Display.pdfDIGITAL3.csv'
        # file=open(name_of_file,'r')
        # df=pd.read_csv(file)
        # newdf=df.dropna(thresh=df.shape[1]-6, axis=0)
        # newdf.to_csv(name_of_file)
        # file=open(name_of_file,'r')
        # inv=CSVInvoiceData.objects.latest('id')
        # csv_reader = csv.DictReader(file)
        # for row in csv_reader:
        #     model=CSVTableData.objects.create(
        #                     Products=row.get('Description of Goods',''),
        #                     HSN_SAC=row.get('HSN/SAC',''),
        #                     GST_rate=row.get('GST',''),
        #                     Rate=row.get('Rate',''),
        #                     quantity=row.get('Quantity',''),
        #                     Discount=row.get('Disc. %',''),
        #                     Amount=row.get('Amount',''),
        #                     Per=row.get('per','')
        #                     )
        #     model.Invoice_data=inv
        #     model.save()
        return Response(status=status.HTTP_201_CREATED)
    def get(self, request, *args, **kwargs):
        query = CSVInvoiceData.objects.latest('id')
        serializer = Getcsvinvoicedata(query)
        return Response(serializer.data)

class TabledataAPI(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        name_of_file=str(settings.BASE_DIR)+'/media/tabula/tabula-Accounting Voucher Display.pdfDIGITAL3.csv'
        file=open(name_of_file,'r')
        df=pd.read_csv(file)
        newdf=df.dropna(thresh=df.shape[1]-6, axis=0)
        newdf.to_csv(name_of_file)
        file=open(name_of_file,'r')
        inv=CSVInvoiceData.objects.latest('id')
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            print(row)
            model=CSVTableData()
            model.Products=row.get('Description of Goods',''),
            model.HSN_SAC=row.get('HSN/SAC',''),
            model.GST_rate=row.get('GST',''),
            model.Rate=row.get('Rate',''),
            model.quantity=row.get('Quantity',''),
            model.Discount=row.get('Disc. %',''),
            model.Amount=row.get('Amount',''),
            model.Per=row.get('per','')
            model.Invoice_data=inv
            model.save()
        return Response(status=status.HTTP_201_CREATED)
    def get(self, request, *args, **kwargs):
        query = CSVInvoiceData.objects.latest('id')
        serializer = Getcsvinvoicedata(query)
        return Response(serializer.data)
class CsvamazonInvoicedataAPI(generics.ListCreateAPIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = FileUploadSerializer
    def post(self, request, *args, **kwargs):
        login_user=request.user
        print(login_user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save(created_by=login_user)
        value=serializer.data['file']
        value1 = str(settings.BASE_DIR)+value
        d: typing.Optional[Document] = None
        l: RegularExpressionTextExtraction = RegularExpressionTextExtraction("Billing Address :")
        m: RegularExpressionTextExtraction = RegularExpressionTextExtraction("Invoice Number :")
        n: RegularExpressionTextExtraction = RegularExpressionTextExtraction("Invoice Date :")
        u: RegularExpressionTextExtraction = RegularExpressionTextExtraction("State/UT Code:")
        f: RegularExpressionTextExtraction = RegularExpressionTextExtraction("Amount in Words:")
        rup: RegularExpressionTextExtraction = RegularExpressionTextExtraction("TOTAL:")
        main_dict={}
        main_file=open(value1, "rb")
        legderlist=[]
        mod=ladgernamedata.objects.all()
        for a in mod:
            legderlist.append(a.ledeger_name)
        try:
            if l:
                d = PDF.loads(main_file, [l])
                assert d is not None
                matches: typing.List[PDFMatch] = l.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(180),
                                            data.get_y() - Decimal(100),
                                            Decimal(400),
                                            Decimal(100))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)
                d = PDF.loads(main_file, [l0])
                assert d is not None
                y=l1.get_text_for_page(0)
                data=''
                for leg in legderlist:
                    if leg[:4] in y:
                        data=leg
            main_dict['Buyer Data']=data
        except:
            pass
        try:
            if m:
                d = PDF.loads(main_file, [m])
                assert d is not None
                matches: typing.List[PDFMatch] = m.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(10),
                                        data.get_y() - Decimal(5),
                                        Decimal(400),
                                        Decimal(10))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])
                assert d is not None
                y=l1.get_text_for_page(0)
            main_dict['Invoice Number']=y
        except:
            pass
        try:
            if n:
                d = PDF.loads(main_file, [n])
                assert d is not None
                matches: typing.List[PDFMatch] = n.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(10),
                                        data.get_y() - Decimal(5),
                                        Decimal(400),
                                        Decimal(10))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])

                assert d is not None
                z=l1.get_text_for_page(0)
            main_dict['Invoice Date']=z
        except:
            pass
        try:
            if u:
                d = PDF.loads(main_file, [u])
                assert d is not None
                matches: typing.List[PDFMatch] = u.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(10),
                                    data.get_y() - Decimal(5),
                                    Decimal(400),
                                    Decimal(10))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])

                assert d is not None
            main_dict['Code']=l1.get_text_for_page(0)
            
        except:
            pass
        try:
            if f:
                d = PDF.loads(main_file, [f])
                assert d is not None
                matches: typing.List[PDFMatch] = f.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(100),
                             data.get_y() - Decimal(20),
                             Decimal(400),
                             Decimal(10))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])

                assert d is not None
                y=l1.get_text_for_page(0)
                try:
                    main_total=w2n.word_to_num(y)
                except Exception as e:
                    nex_txt=''
                    for i,letter in enumerate(y):
                        if i and letter.isupper():
                            nex_txt+=' '
                        nex_txt+=letter
                    main_total=w2n.word_to_num(nex_txt)
            main_dict['Total']=main_total
        except:
            pass
        try:
            if rup:
                d = PDF.loads(main_file, [rup])
                assert d is not None
                matches: typing.List[PDFMatch] = rup.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(100),
                             data.get_y() - Decimal(10),
                             Decimal(575),
                             Decimal(20))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])

                assert d is not None
                z=l1.get_text_for_page(0)
                new=z.replace('�','')
            main_dict['GST Total']=new
        except:
            pass
        print(main_dict)
        for i,j in main_dict.items():
            for r in (("Invoice No.\n", ""), ("Dated\n", ""),("SGST ", ""),("IGST ", ""),("CGST ", ""),("STATETAX(SGST) ", ""),("CENTRALTAX(CGST) ", ""),("Invoice Number : ", ""), ("Invoice Date : ", ""),("State/UT Code: ", ""),("TOTAL: ","")):
                j = str(j).replace(*r)
            main_dict.update({i:j})
        date_list=['%d-%m-%y','%d-%m-%Y','%d/%m/%y','%d/%m/%Y','%d-%b-%Y','%d-%B-%Y','%d-%b-%y','%d-%B-%y','%d/%b/%Y','%d/%B/%Y','%d/%b/%y','%d/%B/%y','%d %b %Y','%d.%m.%Y']
        
        for i in date_list:
            try:
                main_date=datetime.datetime.strptime(main_dict['Invoice Date'], i).date()
            except:
                pass
        inv=CSVInvoiceData.objects.latest('id')
        inv.companyname=main_dict['Buyer Data']
        inv.invoice_no=main_dict['Invoice Number']
        inv.invoice_date=main_date
        igst: RegularExpressionTextExtraction = RegularExpressionTextExtraction("IGST")
        gst=''
        try:
            if igst:
                d = PDF.loads(main_file, [igst])
                assert d is not None
                matches: typing.List[PDFMatch] = igst.get_matches_for_page(0)
                assert len(matches) >= 0
                data=matches[0].get_bounding_boxes()[0]
                r: Rectangle = Rectangle(data.get_x() - Decimal(10),
                             data.get_y() - Decimal(10),
                             Decimal(80),
                             Decimal(20))
                l0: LocationFilter = LocationFilter(r)
                l1: SimpleTextExtraction = SimpleTextExtraction()
                l0.add_listener(l1)

                d = PDF.loads(main_file, [l0])

                assert d is not None
                gst=l1.get_text_for_page(0)
        except:
            pass
        if 'GST Total' in main_dict.keys():
            if 'IGST' in gst:
                inv.IGST=main_dict['GST Total']
                inv.save()
            else:
                s=main_dict['GST Total'].replace(',','')
                amount=float(s)
                cgst=amount/2
                inv.CGST=round(cgst,2)
                inv.SGST=round(cgst,2)
                inv.save()
        else:
            pass
        inv.StateCode=main_dict['Code']
        model1=companydata.objects.get(id=request.data['Company'])
        inv.Company=model1
        inv.subtotal=main_dict['Total']
        inv.file=request.data['file']
        inv.save()
        # name_of_file=str(settings.BASE_DIR)+'/media/tabula/tabula-amz invoice 040421.csv'
        # file=open(name_of_file,'r')
        # df=pd.read_csv(file)
        # file=open(name_of_file,'r')
        # df=pd.read_csv(file)
        # df.columns = [x.strip().replace('\r', '') for x in df.columns]
        # df.columns = [x.strip().replace('\n', '') for x in df.columns]
        # newdf=df.dropna(thresh=df.shape[1]-6, axis=0)
        # newdf = newdf[newdf['Description'] != 'Description']
        # newdf.replace(to_replace="\\r[$&+,:;=?@#|'<>.^*%!-]\₹\d{1,}[.]\d{1,}|\\r\₹\d{1,}[.]\d{1,}|\\r\d{1,}\W|\\rIGST|\\rCGST|\\rSGST|\\r|\\n[$&+,:;=?@#|'<>.^*%!-]\₹\d{1,}[.]\d{1,}|\\n\₹\d{1,}[.]\d{1,}|\\n\d{1,}\W|\\nIGST|\\nCGST|\\nSGST|\\n", value="", regex=True, inplace=True)
        # newdf.to_csv(name_of_file)
        # file=open(name_of_file,'r')
        # inv=CSVInvoiceData.objects.latest('id')
        # csv_reader = csv.DictReader(file)
        # for row in csv_reader:
        #     print('ggg')
        #     model=CSVTableData.objects.create(
        #                     Products=row.get('Description',''),
        #                     HSN_SAC=row.get('HSN/SAC',''),
        #                     GST_rate=row.get('TaxRate',''),
        #                     Rate=row.get('UnitPrice',''),
        #                     quantity=row.get('Qty',''),
        #                     Discount=row.get('Discount',''),
        #                     Amount=row.get('NetAmount',''),
        #                     Per=row.get('per','')
        #                     )
        #     model.Invoice_data=inv
        #     model.save()
        #     print('gfhj')
        return Response(status=status.HTTP_201_CREATED)
    def get(self, request, *args, **kwargs):
        query = CSVInvoiceData.objects.latest('id')
        serializer = Getcsvinvoicedata(query)
        return Response(serializer.data)
class AmazonTabledataAPI(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        name_of_file=str(settings.BASE_DIR)+'/media/tabula/tabula-Accounting Voucher Display.pdfDIGITAL3.csv'
        file=open(name_of_file,'r')
        df=pd.read_csv(file)
        newdf=df.dropna(thresh=df.shape[1]-6, axis=0)
        newdf.to_csv(name_of_file)
        file=open(name_of_file,'r')
        inv=CSVInvoiceData.objects.latest('id')
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            print(row)
            model=CSVTableData()
            model.Products=row.get('Description of Goods',''),
            model.HSN_SAC=row.get('HSN/SAC',''),
            model.GST_rate=row.get('GST',''),
            model.Rate=row.get('Rate',''),
            model.quantity=row.get('Quantity',''),
            model.Discount=row.get('Disc. %',''),
            model.Amount=row.get('Amount',''),
            model.Per=row.get('per','')
            model.Invoice_data=inv
            model.save()
        return Response(status=status.HTTP_201_CREATED)
    def get(self, request, *args, **kwargs):
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PaymentVoucherentry(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = PaymentVoucherDataSerializer
    def post(self, request, format=None):
        li=[]
        model=ladgernamedata.objects.all()
        for mod in model:
            li.append(mod.ledeger_name)
        serializer = PaymentVoucherDataSerializer(data=request.data)
        p = re.compile(r'(?:Rs\.?|INR)\s*(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s*(?:Rs\.?|INR)')
        regEx = r'(\d{2}[\/ -](\d{2}|January|Jan|JAN|February|Feb|FEB|March|Mar|MAR|April|Apr|APR|May|May|MAY|June|Jun|JUN|July|Jul|JUL|August|Aug|AUG|September|Sep|SEP|October|Oct|OCT|November|Nov|NOV|December|Dec|DEC)[\/ -]\d{2,4})'
        s=request.data['Narration']
        x=p.findall(s)
        result = re.findall(regEx,s)
        serializer.is_valid()
        date_list=['%d-%m-%y','%d-%m-%Y','%d/%m/%y','%d/%m/%Y','%d-%b-%Y','%d-%B-%Y','%d-%b-%y','%d-%B-%y','%d/%b/%Y','%d/%B/%Y','%d/%b/%y','%d/%B/%y','%d %b %Y','%d %B %Y','%d %b %y','%d %B %y','%B %d,%Y','%d %B,%Y']
        if 'debited' in s or 'Debited' in s or 'transferred to' in s or 'sent to' in s or 'made a payment' in s:
            if result:
                dates=result[0][0]
                for i in date_list:
                    try:
                        x=datetime.datetime.strptime(dates, i).date()
                    except:
                        pass
                for l in li:
                    if (s.__contains__(l)):
                        m=VoucherInvoiceEntry(Narration=s,Voucher_date=x,legdername=l,Voucher_amount_dr=0.00,Voucher_amount_cr=x[0][0])
                        m.save()
                        break
                    else:
                        m=VoucherInvoiceEntry(Narration=s,Voucher_date=x,legdername='',Voucher_amount_dr=0.00,Voucher_amount_cr=x[0][0])
                        m.save()
                        break
            else:
                for l in li:
                    if (s.__contains__(l)):
                        m=VoucherInvoiceEntry(Narration=s,Voucher_date=None,legdername=l,Voucher_amount_dr=0.00,Voucher_amount_cr=x[0][0])
                        m.save()
                        break
                    else:
                        m=VoucherInvoiceEntry(Narration=s,Voucher_date=None,legdername='',Voucher_amount_dr=0.00,Voucher_amount_cr=x[0][0])
                        m.save()
                        break

        elif 'credited' in s or 'Credited' in s or 'transferred from' in s:
            print(x[0][0],'Credited')
            if result:
                dates=result[0][0]
                for i in date_list:
                    try:
                        x=datetime.datetime.strptime(dates, i).date()
                    except:
                        pass
                for l in li:
                    if (s.__contains__(l)):
                        m=VoucherInvoiceEntry(Narration=s,Voucher_date=x,legdername=l,Voucher_amount_dr=x[0][0],Voucher_amount_cr=0.00)
                        m.save()
                        break
                    else:
                        m=VoucherInvoiceEntry(Narration=s,Voucher_date=x,legdername='',Voucher_amount_dr=x[0][0],Voucher_amount_cr=0.00)
                        m.save()
                        break
            else:
                for l in li:
                    if (s.__contains__(l)):
                        m=VoucherInvoiceEntry(Narration=s,Voucher_date=None,legdername=l,Voucher_amount_dr=x[0][0],Voucher_amount_cr=0.00)
                        m.save()
                        break
                    else:
                        m=VoucherInvoiceEntry(Narration=s,Voucher_date=None,legdername='',Voucher_amount_dr=x[0][0],Voucher_amount_cr=0.00)
                        m.save()
                        break

        else:
            pass
        
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PaymentVouchereditdelete(APIView):
    """
    Retrieve, update or delete a org instance.
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = PaymentVoucherDataSerializer1
    def get_object(self,pk):
        try:
            return VoucherInvoiceEntry.objects.get(pk=pk)
        except VoucherInvoiceEntry.DoesNotExist:
            raise Http404

    def get(self, request, pk,format=None):
        snippet = self.get_object(pk=pk)
        serializer = PaymentVoucherDataSerializer1(snippet)
        return Response(serializer.data)

    def put(self, request,pk,format=None):
        snippet = self.get_object(pk=pk)
        serializer = PaymentVoucherDataSerializer1(snippet, data=request.data)
        if serializer.is_valid():
            snippet.Voucher_amount_dr=request.data['Voucher_amount_dr']
            x=request.data['Voucher_amount_dr']
            snippet.Voucher_amount_dr=-float(x)
            snippet.save()
            serializer.save(is_verified=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk,format=None):
        snippet = self.get_object(pk=pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








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
