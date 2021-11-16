from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
import requests
import xml.etree.ElementTree as ET
from .models import ladgernamedata,companydata
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm)
import xml.etree.cElementTree as ET
from xml.etree import ElementTree
from accountapp.models import User
# from .demo import MainWindow
# Create your views here.
import socket

# Python Program to Get IP Address
import socket   
import netifaces as ni
from getmac import get_mac_address as gma
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,api_view
import psutil,os
import netifaces

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_ledeger(request):
    login_user=request.user
    if request.user.is_superuser:
        model=companydata.objects.filter(user_company=login_user)
        for x in model:
            url='http://'+ x.comp_ip_address+':9000'
            data="<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE><ID>List of Ledgers</ID>"
            data+="</HEADER><BODY><DESC><STATICVARIABLES><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT></STATICVARIABLES></DESC></BODY></ENVELOPE>"
            request=requests.post(url=url,data=data)
            print(data)
            response=request.text.strip().replace("&amp;","and")
            responseXML = ET.fromstring(response)
            print(response)
            namedata=[]
            data2=ladgernamedata.objects.filter(created_by=login_user)
            for i in data2:
                namedata.append(i.ledeger_name)
            for data in responseXML.findall('./BODY/DATA/COLLECTION/LEDGER'):
                getdata=(data.get('NAME'))
                data1=getdata
                print("%%%%%%%%%%%",data1)
                if data1 not in namedata:
                    dbsave=ladgernamedata(ledeger_name=data1,created_by=login_user)
                    dbsave.save()
    else:               
        user_model=User.objects.filter(created_by__icontains=login_user.created_by)
        for x in user_model:
            model=companydata.objects.filter(user_company=x)
            for y in model:
                comp=str(y)
                getdata=''
                url='http://'+ y.comp_ip_address+':9000'
                data = '<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE>'
                data += '<ID>ListOfCompanies</ID></HEADER><BODY><DESC><STATICVARIABLES><SVCurrentCompany>Digital Docsys Pvt Ltd</SVCurrentCompany><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>'
                data += '</STATICVARIABLES><TDL><TDLMESSAGE><COLLECTION Name="ListOfCompanies"><TYPE>Company</TYPE>'
                data += '<FETCH>Name,CompanyNumber</FETCH></COLLECTION></TDLMESSAGE></TDL></DESC></BODY></ENVELOPE>'
                req = requests.post(url=url, data=data)
                res = Et.fromstring(req.text.strip())
                for cmp in res.findall('./BODY/DATA/COLLECTION/COMPANY'):
                    getdata=(cmp.find('NAME').text)
                print(getdata,comp)
                if getdata==comp:
                    url='http://'+ y.comp_ip_address+':9000'
                    data="<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE><ID>List of Ledgers</ID>"
                    data+="</HEADER><BODY><DESC><STATICVARIABLES><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT></STATICVARIABLES></DESC></BODY></ENVELOPE>"
                    request=requests.post(url=url,data=data)
                    print(data)
                    response=request.text.strip().replace("&amp;","and")
                    responseXML = ET.fromstring(response)
                    print(response)
                    namedata=[]
                    data2=ladgernamedata.objects.filter(created_by=login_user)
                    for i in data2:
                        namedata.append(i.ledeger_name)
                    for data in responseXML.findall('./BODY/DATA/COLLECTION/LEDGER'):
                        getdata=(data.get('NAME'))
                        data1=getdata
                        print("%%%%%%%%%%%",data1)
                        if data1 not in namedata:
                            dbsave=ladgernamedata(ledeger_name=data1,created_by=login_user)
                            dbsave.save()
    return HttpResponse(status=status.HTTP_200_OK)
    
from xml.etree import ElementTree as Et

from uuid import getnode as get_mac
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_company_name(request):
    login_user=request.user
    x=''
    interfaces = ni.interfaces()
    interfaces = netifaces.interfaces()
    interfaces.remove('lo')
    out_interfaces = dict()
    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        out_addrs = dict()
        if netifaces.AF_INET in addrs.keys():
            out_addrs["ipv4"] = addrs[netifaces.AF_INET]
        out_interfaces[interface] = out_addrs
        x=out_interfaces['enp6s0']['ipv4'][0]['addr']
    mac_address=gma()
    url="http://"+x+":9000"
    print("$$$$$$$$$$$$$$yyyggggy444",login_user)
    data = '<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE>'
    data += '<ID>ListOfCompanies</ID></HEADER><BODY><DESC><STATICVARIABLES><SVCurrentCompany>Digital Docsys Pvt Ltd</SVCurrentCompany><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>'
    data += '</STATICVARIABLES><TDL><TDLMESSAGE><COLLECTION Name="ListOfCompanies"><TYPE>Company</TYPE>'
    data += '<FETCH>Name,CompanyNumber</FETCH></COLLECTION></TDLMESSAGE></TDL></DESC></BODY></ENVELOPE>'
    req = requests.post(url=url, data=data)
    res = Et.fromstring(req.text.strip())
    namedata=[]
    data2=companydata.objects.filter(user_company=login_user)
    for i in data2:
        print("****************",i.comp_name)
        namedata.append(i.comp_name)
    for cmp in res.findall('./BODY/DATA/COLLECTION/COMPANY'):
        getdata=(cmp.find('NAME').text)
        getdata1=(cmp.find('COMPANYNUMBER').text)
        comname=getdata
        compid=getdata1
        print("CCCCCCCCCCCCCCCCCCCC",getdata)
        print("CCCCCCCCCCCCCCCCCCCCrrr",getdata1)
        if getdata not in namedata:
            dbsave=companydata(comp_name=comname,comp_id=compid,user_company=login_user,comp_ip_address=x,mac_ad=mac_address)
            dbsave.save() 
    return HttpResponse({'data1':'sucefully fetch data from tally'})     
  

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# @csrf_exempt
# def create_ladeger(request,format=None):
#     try:
#         print("yyyyyyyyyyyyyyyyyyyyyy")
#         led_name = request.POST.get('led_name','')
#         print("submit",led_name)
#         led_group=request.POST.get('led_group','')
#         print("OOOOOOOOOOOOOOOOOOOOOOO")
#         led_address=request.POST.get('led_address','')
#         print("^^^^^^^^^^^^",led_address)
#         led_country=request.POST.get('led_country','')
#         print("&**********************",led_country)
#         led_state=request.POST.get('led_state','')
#         print("^^^^^^^^^^^^^^^^^",led_state)
#         led_mobile=request.POST.get('led_mobile','')
#         print("TTTTTTTTTTTTTTT",led_mobile)
#         led_gst=request.POST.get('led_gst','')
#         url="http://192.168.1.105:9000"
#         data = '<ENVELOPE><HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER><BODY>'
#         data += '<IMPORTDATA><REQUESTDESC><REPORTNAME>All Masters</REPORTNAME></REQUESTDESC><REQUESTDATA>'
#         data += '<TALLYMESSAGE xmlns:UDF="TallyUDF"><LEDGER Action="Create"><NAME>'+led_name+'</NAME><PARENT>'+led_group
#         data += '</PARENT><ADDRESS>'+led_address+'</ADDRESS><COUNTRYOFRESIDENCE>'+led_country+'</COUNTRYOFRESIDENCE>'
#         data += '<LEDSTATENAME>'+led_state+'</LEDSTATENAME><LEDGERMOBILE>'+led_mobile+'</LEDGERMOBILE><PARTYGSTIN>'
#         data += led_gst+'</PARTYGSTIN></LEDGER></TALLYMESSAGE></REQUESTDATA></IMPORTDATA></BODY></ENVELOPE>'
#         print("%%%%%%%%%%%%%%%%",data)
#         req = requests.post(url=url, data=data)
#         return HttpResponse("sucefully")  
#         # return render(request,'booking/bmr.html',{'req':req})  
#     except Exception as e:
#         raise e
@csrf_exempt
def create_ladeger_with_company(request,format=None):
    try:
        print("yyyyyyyyyyyyyyyyyyyyyy")
        led_name = request.POST.get('led_name','')
        print("submit",led_name)
        led_group=request.POST.get('led_group','')
        print("OOOOOOOOOOOOOOOOOOOOOOO")
        led_address=request.POST.get('led_address','')       
        # url="http://192.168.1.105:9000"
        # url="http://192.168.29.7:9000"
        url='http://192.168.29.141:9000'
        data='<ENVELOPE><HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>'
        data+='<BODY><IMPORTDATA><REQUESTDESC><REPORTNAME>ALL MASTERS</REPORTNAME>'
        data+='<STATICVARIABLES><SVCURRENTCOMPANY>Abcd</SVCURRENTCOMPANY></STATICVARIABLES>'
        data+='</REQUESTDESC><REQUESTDATA><TALLYMESSAGE xmlns:UDF="TallyUDF"><LEDGER  ACTION="Create"><NAME>'+led_name+'</NAME>'
        data+='<PARENT>'+led_group+'</PARENT><ADDRESS>'+led_address+'</ADDRESS>'                       
        data+='</LEDGER></TALLYMESSAGE></REQUESTDATA></IMPORTDATA></BODY></ENVELOPE>'
        print("%%%%%%%%%%%%%%%%",data)
        req = requests.post(url=url, data=data)
        print(req)
        # return HttpResponse("sucefully")  
        return render(request,'booking/bmr.html',{'req':req})  
    except Exception as e:
        raise e


@csrf_exempt          
def voucher_entery(request):
    try:
        # data=ladger_name.objects.all()
        # ladeger_name=data
        led_date = request.POST.get('led_date','')
        print("ddddddddd",led_date)
        naration=request.POST.get('naration','')
        ladeger_name=request.POST.get('ladeger_name','')
        led_dr=request.POST.get('led_dr','')
        print("drdrdrdrdrdrdr",led_dr)
        bank_name=request.POST.get('bank_name','')
        led_cr=request.POST.get('led_cr','')
        companyname="Abcd"
        # url="http://192.168.1.105:9000"
        # url="http://192.168.29.7:9000"
        url='http://192.168.29.141:9000'
        data='<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>Import</TALLYREQUEST><TYPE>Data</TYPE><ID>Vouchers</ID></HEADER>'
                
        data+='<BODY><DESC><STATICVARIABLES><SVCURRENTCOMPANY>'+companyname+'</SVCURRENTCOMPANY></STATICVARIABLES></DESC><DATA>'

        data+='<TALLYMESSAGE><VOUCHER><DATE>'+led_date
        data+='</DATE><NARRATION>'+naration
        data+='</NARRATION><VOUCHERTYPENAME>Payment</VOUCHERTYPENAME>'
       
        data+='<ALLLEDGERENTRIES.LIST><LEDGERNAME>'+ladeger_name
        data+='</LEDGERNAME><ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>'
        data+='<AMOUNT>'+led_dr
        data+='</AMOUNT></ALLLEDGERENTRIES.LIST><ALLLEDGERENTRIES.LIST>'
        data+='<LEDGERNAME>'+bank_name
        data+='</LEDGERNAME><ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>'
        data+='<AMOUNT>'+led_cr
        data+='</AMOUNT></ALLLEDGERENTRIES.LIST></VOUCHER>'
        data+='</TALLYMESSAGE></DATA></BODY></ENVELOPE>'
        print(data)
        print(url)
        req = requests.post(url=url, data=data)
        print(req)
        # return HttpResponse("sucefully")
        
        return render(request,'booking/voucher.html',{'req':req})
    except Exception as e:
        raise e      

@csrf_exempt 
def creategrup(request):
    # url="http://192.168.1.105:9000"
    url='http://192.168.29.141:9000'
    grp_name = request.POST.get('grp_name','')                                 
    print("ddddddddd",grp_name)
    main_grp=request.POST.get('main_grp','')
    ladeger_name=request.POST.get('ladeger_name','')
    open_bal=request.POST.get('open_bal','')
    open_bal=request.POST.get('open_bal','')
    # grup_name=request.POST.get('grup_name','')      
    print("HHHHHHHHHHH",open_bal)
    url="http://192.168.1.105:9000"
    data='<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>Import</TALLYREQUEST><TYPE>Data</TYPE><ID>All Masters</ID></HEADER>'
    data+='<BODY><DESC></DESC><DATA><TALLYMESSAGE><GROUP><NAME>'+grp_name
    data+='</NAME><PARENT>'+main_grp
    data+='</PARENT></GROUP><LEDGER><NAME>'+ladeger_name
    data+='</NAME><PARENT>'+grp_name
    data+='</PARENT><OPENINGBALANCE>'+open_bal
    data+='</OPENINGBALANCE></LEDGER></TALLYMESSAGE></DATA></BODY></ENVELOPE>'
    print(data)
    req = requests.post(url=url, data=data)
    return HttpResponse("sucefully submited")

############################# django restframework start here  #################################
from tallyapp.models import ladgernamedata
from tallyapp.serializers import UpdateCompanySerializer, ladegerSerializer,CompanySerializer,UpdateLegderSerializer,NormalCompanySerializer,PostladegerSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class ladegerList(APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ladegerSerializer
    def get(self, request, format=None):
        login_user=request.user
        snippets = ladgernamedata.objects.all()
        serializer = ladegerSerializer(snippets, many=True)
        return Response(serializer.data)
class LegderPost(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostladegerSerializer
    def get(self, request, format=None):
        snippets = ladgernamedata.objects.all()
        print(snippets)
        serializer = PostladegerSerializer(snippets, many=True)
        print(serializer)
        return Response(serializer.data)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CompanyList(APIView):
    # authentication_classes = (SessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerializer
    def get(self, request, format=None):
        try:
            login_user=request.user
            # snippets = companydata.objects.filter(user_company=login_user)
            snippets=companydata.objects.all()
            serializer = CompanySerializer(snippets, many=True)
            return Response(serializer.data)
        except Exception as e:
           return HttpResponse("something get worn please cntect admin")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT) 

class NormalCompanyList(APIView):
    # authentication_classes = (SessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
    serializer_class = NormalCompanySerializer
    def get(self, request, format=None):
        try:
            login_user=request.user
            # snippets = companydata.objects.filter(user_company=login_user)
            snippets=companydata.objects.all()
            serializer = NormalCompanySerializer(snippets, many=True)
            return Response(serializer.data)
        except Exception as e:
           return HttpResponse("something get worn please cntect admin")       
class UpdateCompany(APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return companydata.objects.get(pk=pk)
        except companydata.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UpdateCompanySerializer(snippet)
        return Response(serializer.data)
    
    def patch(self, request,pk, *args, **kwargs):
        snippet = self.get_object(pk)
        serializer = UpdateCompanySerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status.HTTP_204_NO_CONTENT)
class UpdateLegder(APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return ladgernamedata.objects.get(pk=pk)
        except ladgernamedata.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UpdateLegderSerializer(snippet)
        return Response(serializer.data)
    
    def patch(self, request,pk, *args, **kwargs):
        snippet = self.get_object(pk)
        serializer = UpdateLegderSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# def voucher_entery(request):#'20080402
  
#     # data=ladger_name.objects.all()
#     # ladeger_name=data
#     led_date = request.POST.get('led_date','')
#     print("ddddddddd",led_date)
#     # naration=request.POST.get('naration','')
#     ladeger_name=request.POST.get('ladeger_name','')
#     led_dr=request.POST.get('led_dr','')
#     print("drdrdrdrdrdrdr",led_dr)
#     bank_name=request.POST.get('bank_name','')
#     led_cr=request.POST.get('led_cr','')
#     url="http://192.168.1.105:9000"

#     data = "<ENVELOPE>" 
#     data += "<HEADER>" 
#     data += "<TALLYREQUEST>Import Data</TALLYREQUEST>" 
#     data += "</HEADER>" 
#     data += "<BODY>" 
#     data += "<IMPORTDATA>" 
#     data += "<REQUESTDESC>" 
#     data += "<REPORTNAME>Vouchers</REPORTNAME>" 
#     data += "<STATICVARIABLES>" 
#     data += "<SVCURRENTCOMPANY>##SVCURRENTCOMPANY</SVCURRENTCOMPANY>" 
#     data += "</STATICVARIABLES>" 
#     data += "</REQUESTDESC>" 
#     data += "<REQUESTDATA>" 
#     data += "<TALLYMESSAGE xmlns:UDF=" + "\"" + "TallyUDF" + "\" >" 
#     data += "<VOUCHER VCHTYPE=" + "\"" + "Purchase" + "\" >" 
#     data += '<DATE>" 20210501 "</DATE>' 
#     data += "<VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>" 
#     data += "<VOUCHERNUMBER>"1"</VOUCHERNUMBER>" 
 
#     data += "<ALLLEDGERENTRIES.LIST>" 
#     data += "<LEDGERNAME>" + strSupplierName + "</LEDGERNAME>" 
#     data += "<GSTCLASS/>" 
#     data += "<ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>" 
#     data += "<LEDGERFROMITEM>No</LEDGERFROMITEM>" 
#     data += "<REMOVEZEROENTRIES>No</REMOVEZEROENTRIES>" 
#     data += "<ISPARTYLEDGER>Yes</ISPARTYLEDGER>" 
#     data += "<AMOUNT>" + strGRN + "</AMOUNT>" 
#     data += "<BILLALLOCATIONS.LIST>" 
#     data += "<NAME>" + strGRNNo + "</NAME>" 
#     data += "<BILLCREDITPERIOD>30 Days</BILLCREDITPERIOD>" 
#     data += "<BILLTYPE>New Ref</BILLTYPE>" 
#     data += "<AMOUNT>" + strGRN + "</AMOUNT>" 
#     data += "</BILLALLOCATIONS.LIST>" 
#     data += "</ALLLEDGERENTRIES.LIST>" 
#     data += "<ALLLEDGERENTRIES.LIST>" 
#     data += "<LEDGERNAME>Abhinav Sharma</LEDGERNAME>" 
#     data += "<GSTCLASS/>" 
#     data += "<ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>" 
#     data += "<LEDGERFROMITEM>No</LEDGERFROMITEM>" 
#     data += "<REMOVEZEROENTRIES>No</REMOVEZEROENTRIES>" 
#     data += "<ISPARTYLEDGER>No</ISPARTYLEDGER>" 
#     data += "<AMOUNT>" + strGRNValueNtv + "</AMOUNT>" 
#     data += "</ALLLEDGERENTRIES.LIST>" 
#     data += "</VOUCHER>" 
#     data += "</TALLYMESSAGE>" 
#     data += "</REQUESTDATA>" 
#     data += "</IMPORTDATA>" 
#     data += "</BODY>" 
#     data += "</ENVELOPE>" 

    
#     req = requests.post(url=url, data=data)
#     return render(request,'booking/voucher.html',{'req':req}) 
