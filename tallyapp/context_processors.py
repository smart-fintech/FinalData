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
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.etree import ElementTree as Et
from uuid import getnode as get_mac
# from .demo import MainWindow
# Create your views here.

def get_ledeger_auto(request):
    if request.user.is_authenticated:
        login_user=request.user
        print("$$$$$$$$$$$$$$444",login_user)
        # url="http://localhost:9999"
        # url="http://192.168.29.7:9000"
        url='http://192.168.29.141:9000'
        print("$$$$$$$$33333333333$$$$$$444",login_user)
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
                print("dartahjoijijij")
        return({'data1':' sucefully fetchdata from tally'})
    return({'data':'somethink went worng try again '})



def get_company_name_auto(request):
    if request.user.is_authenticated:
        login_user=request.user
        print("$$$$$$$$$$$$$$yyyy444",login_user)
        # url="http://localhost:9999"
        # url="http://192.168.1.105:9000"
        url='http://192.168.29.141:9000'
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
                dbsave=companydata(comp_name=comname,comp_id=compid,user_company=login_user)
                dbsave.save() 
        return({'data1':'sucefully fetch data from tally'})
    return({'data':'some problem please try again'})       
