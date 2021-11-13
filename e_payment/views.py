
from django.db.models import query
from django.http import HttpResponse,Http404
from rest_framework import views
from .models import EpaymentDetails, ShowData,LedgerData,BankDetails,masterBank
import re
import os.path
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
import pandas as pd
from .serializers import EpaymentSerializer,UpdateBankDataSerializer, LedgerDataSerializer1,LedgerDataSerializer,ShowDataSerializer1,ShowBankDataSerializer,EpaymentSerializer1,ShowDataSerializer,BankDataSerializer,masterBankSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
import os,csv
import shutil
from rest_framework import status
from django.conf import settings
# import tabula
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from tallyapp.models import companydata, ladgernamedata
import requests
import xml.etree.ElementTree as ET
import datetime,pathlib,pdfkit,tabula
# import pdfkit

class BankDetailsViews1(APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        queryset=EpaymentDetails.objects.all()
        print(queryset)
        serializer = EpaymentSerializer1(queryset, many=True)
        return Response(serializer.data)
class BankDetailsViews2(APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        login_user=request.user
#         queryset2=companydata.objects.filter(user_company=login_user)
#         for i in queryset2:
#             queryset=BankDetails.objects.filter(comp_name=i)
#             print(queryset)
        queryset=BankDetails.objects.all()
        serializer = ShowBankDataSerializer(queryset, many=True)
        return Response(serializer.data)
    
class MasterbankViews(generics.ListAPIView):

    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset=masterBank.objects.all()
    serializer_class=masterBankSerializer
    def get(self,request):
        queryset = self.get_queryset()
        serializer = masterBankSerializer(queryset, many=True)
        return Response(serializer.data)

class BankDetailsViews(generics.ListAPIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset=BankDetails.objects.all()
    serializer_class=BankDataSerializer
    def get(self,request):
        queryset = self.get_queryset()
        serializer = BankDataSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateBankdetails(APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return BankDetails.objects.get(pk=pk)
        except BankDetails.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UpdateBankDataSerializer(snippet)
        return Response(serializer.data)
    
    def patch(self, request,pk, *args, **kwargs):
        snippet = self.get_object(pk)
        serializer = UpdateBankDataSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EpaymentDataPost(generics.ListCreateAPIView):
#     authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset=EpaymentDetails.objects.all()
    serializer_class=EpaymentSerializer
    def post(self,request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['file']
        serializer.save()
        user_data=serializer.data
        value = str(settings.BASE_DIR)+user_data['file']
        extension = os.path.splitext(value)[1][1:]
        if extension=='pdf':
            print(value)
            tabula.convert_into(value, "media/tabula/idbi.csv",output_format="csv", pages='all',stream=True)
            def remove1():
                x=0
                with open('media/tabula/idbi.csv', 'r') as f:
                    csv_reader = csv.reader(f)
                    for index,row in enumerate(csv_reader):
                        if 'Date' in row:
                            x=index
                            break
                        elif 'Value Date' in row:
                            x=index
                            break
                        elif 'Transaction Date' in row:
                            x=index
                            break
                        else:
                            pass
                return x
            diff=remove1()
            
            df=pd.read_csv('media/tabula/idbi.csv', names=range(10))
            df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["",""], regex=True, inplace=True)
            t=df.loc[diff:]
            t.columns=t.iloc[0]
            t=t.reset_index(drop=True)
            for i in t.columns:
                t = t[t[i] != i]
            for col in t.columns:
                if col=='Date':
                    break
                elif col=='Txn Date':
                    t.rename(columns = {"Txn Date": "Date"}, inplace = True)
                    break
                elif col=='Transaction Date':
                    t.rename(columns = {"Transaction Date": "Date"}, inplace = True)
                    break
            x=''
            
            for d in t.columns:
                if d=='Date': 
                    x=d
            t=t[t[x] != x]
            t.dropna(subset = [x],axis=0,inplace=True)
            t[x]= pd.to_datetime(t[x], errors='coerce')
            try:
                t['Credit'] = t.apply(lambda x: x['Amount'] if (x['Type'] == 'Credit' or x['Type'] == 'Cr' or x['Type'] == 'CR') else '', axis = 1)
                t['Debit'] = t.apply(lambda x: x['Amount'] if (x['Type'] == "Debit" or x['Type'] =='Dr' or x['Type'] =='DR') else '', axis = 1)
                t['Withdrawals'] = t['Withdrawals'].str.replace(',', '').astype(float)
                t['Deposits'] = t['Deposits'].str.replace(',', '').astype(float)
            except:
                pass
            try:
                df1 = t.loc[t['Amount'].str.contains("Cr", case=False)]
                t['Credit'] = df1['Amount'].str.extract(r'([\d:,.]+)')
                df2 = t.loc[t['Amount'].str.contains("Dr", case=False)]
                t['Debit'] = df2['Amount'].str.extract(r'([\d:,.]+)')
                t.drop('Amount', inplace=True, axis=1)
            except:
                pass
            t.to_csv('media/'+'new.csv',index=False)
            value1 = 'media/new.csv'
            dst='media/prevois/'+'new.csv'
            data=shutil.copyfile(value1,dst)
            with open('media/prevois/new.csv') as csv_file:
                df=pd.read_csv(csv_file)
                for col in df.columns:
                    if col=='Narration':
                        pass
                    elif col=='Details':
                        df.rename(columns = {"Details": "Narration"}, inplace = True)
                    elif col=='Description':
                        df.rename(columns = {"Description": "Narration"}, inplace = True)
                    elif col=='Transactions':
                        df.rename(columns = {"Transactions": "Narration"}, inplace = True)
                    elif col=='Particulars':
                        df.rename(columns = {"Particulars": "Narration"}, inplace = True)
                    elif col=='Transaction Details':
                        df.rename(columns = {"Transaction Details": "Narration"}, inplace = True)
                    elif col=='Transaction Remarks':
                        df.rename(columns = {"Transaction Remarks": "Narration"}, inplace = True)
                    elif col=='Remarks':
                        df.rename(columns = {"Remarks": "Narration"}, inplace = True)
                    elif col=='Ref.No':
                        pass
                    elif col=='Chq./Ref.No.':
                        df.rename(columns = {"Chq./Ref.No.": "Ref.No"}, inplace = True)
                    elif col=='Cheque/Ref No.':
                        df.rename(columns = {"Cheque/Ref No.": "Ref.No"}, inplace = True)
                    elif col=='Ref No./Cheque\rNo.':
                        df.rename(columns = {"Ref No./Cheque\rNo.": "Ref.No"}, inplace = True)
                    elif col=='Ref No./ChequeNo.':
                        df.rename(columns = {"Ref No./ChequeNo.": "Ref.No"}, inplace = True)
                    elif col=='Ref No./Cheque\nNo.':
                        df.rename(columns = {"Ref No./Cheque\nNo.": "Ref.No"}, inplace = True)
                    elif col=='Txn No.':
                        df.rename(columns = {"Txn No.": "Ref.No"}, inplace = True)
                    elif col=='Tran Id':
                        df.rename(columns = {"Tran Id": "Ref.No"}, inplace = True)
                    elif col=='Debit':
                        pass
                    elif col=='Withdrawal Amt.':
                        df.rename(columns = {"Withdrawal Amt.": "Debit"}, inplace = True)
                    elif col=='Withdrawal Amount\n(INR)':
                        df.rename(columns = {"Withdrawal Amount\n(INR)": "Debit"}, inplace = True)
                    elif col=='Withdrawal Amount':
                        df.rename(columns = {"Withdrawal Amount": "Debit"}, inplace = True)
                    elif col=='Withdrawals':
                        df.rename(columns = {"Withdrawals": "Debit"}, inplace = True)
                    elif col=='Withdrawal':
                        df.rename(columns = {"Withdrawal": "Debit"}, inplace = True)
                    elif col=='Decrease':
                        df.rename(columns = {"Decrease": "Debit"}, inplace = True)
                    elif col=='Credit':
                        pass
                    elif col=='Deposit Amt.':
                        df.rename(columns = {"Deposit Amt.": "Credit"}, inplace = True)
                    elif col=='Deposit Amount\n(INR)':
                        df.rename(columns = {"Deposit Amount\n(INR)": "Debit"}, inplace = True)
                    elif col=='Deposit Amount':
                        df.rename(columns = {"Deposit Amount": "Credit"}, inplace = True)
                    elif col=='Deposit':
                        df.rename(columns = {"Deposit": "Credit"}, inplace = True)
                    elif col=='Deposits':
                        df.rename(columns = {"Deposits": "Credit"}, inplace = True)
                    elif col=='Increase':
                        df.rename(columns = {"Increase": "Credit"}, inplace = True)
                    elif col=='Date':
                        pass
                    elif col=='Tran Date':
                        df.rename(columns = {"Tran Date": "Date"}, inplace = True)
                    elif col=='Txn Date':
                        df.rename(columns = {"Txn Date": "Date"}, inplace = True)
                    elif col=='Transaction Date':
                        df.rename(columns = {"Transaction Date": "Date"}, inplace = True)
                    elif col=='Balance':
                        pass
                    elif col=='Closing Balance':
                        df.rename(columns = {"Closing Balance": "Balance"}, inplace = True)
                    elif col=='Closing Bal':
                        df.rename(columns = {"Closing Bal": "Balance"}, inplace = True)
                    elif col=='Closing Bal.':
                        df.rename(columns = {"Closing Bal.": "Balance"}, inplace = True)
                def rolling_group(val):
                    if pd.notnull(val): rolling_group.group +=1 
                    return rolling_group.group
                rolling_group.group = 0 
                def joinFunc(g,column):
                    col =g[column]
                    joiner = "/" if column == "Date" else ""
                    s = joiner.join([str(each) for each in col if pd.notnull(each)])
                    s = re.sub("(?<=&)"+joiner," ",s)
                    s = re.sub("(?<=-)"+joiner,"",s)
                    s = re.sub(joiner*2,joiner,s)   
                    return s
                groups = df.groupby(df['Date'].apply(rolling_group),as_index=False)
                groupFunct = lambda g: pd.Series([joinFunc(g,col) for col in g.columns],index=g.columns)
                x=groups.apply(groupFunct)
                x.to_csv('media/new.csv')
            df=pd.read_csv('media/new.csv',thousands=',')
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            df['Bank']=user_data['bankname']
            df.to_csv('media/output.csv')
            os.remove('media/prevois/new.csv')
            os.remove('media/new.csv')
        else:
            df=pd.read_csv(value, names=range(10))
            try:
                df['Credit'] = df.apply(lambda x: x['Amount'] if (x['Type'] == 'Credit' or x['Type'] == 'Cr' or x['Type'] == 'CR') else '', axis = 1)
                df['Debit'] = df.apply(lambda x: x['Amount'] if (x['Type'] == "Debit" or x['Type'] =='Dr' or x['Type'] =='DR') else '', axis = 1)
                df['Withdrawals'] = df['Withdrawals'].str.replace(',', '').astype(float)
                df['Deposits'] = df['Deposits'].str.replace(',', '').astype(float)
            except:
                pass
            with open(value) as csv_file:
                df=pd.read_csv(csv_file)
                for col in df.columns:
                    if col=='Narration':
                        pass
                    elif col=='Details':
                        df.rename(columns = {"Details": "Narration"}, inplace = True)
                    elif col=='Description':
                        df.rename(columns = {"Description": "Narration"}, inplace = True)
                    elif col=='Transactions':
                        df.rename(columns = {"Transactions": "Narration"}, inplace = True)
                    elif col=='Particulars':
                        df.rename(columns = {"Particulars": "Narration"}, inplace = True)
                    elif col=='Transaction Details':
                        df.rename(columns = {"Transaction Details": "Narration"}, inplace = True)
                    elif col=='Transaction Remarks':
                        df.rename(columns = {"Transaction Remarks": "Narration"}, inplace = True)
                    elif col=='Remarks':
                        df.rename(columns = {"Remarks": "Narration"}, inplace = True)
                    elif col=='Ref.No':
                        pass
                    elif col=='Chq./Ref.No.':
                        df.rename(columns = {"Chq./Ref.No.": "Ref.No"}, inplace = True)
                    elif col=='Cheque/Ref No.':
                        df.rename(columns = {"Cheque/Ref No.": "Ref.No"}, inplace = True)
                    elif col=='Ref No./Cheque\rNo.':
                        df.rename(columns = {"Ref No./Cheque\rNo.": "Ref.No"}, inplace = True)
                    elif col=='Ref No./ChequeNo.':
                        df.rename(columns = {"Ref No./ChequeNo.": "Ref.No"}, inplace = True)
                    elif col=='Ref No./Cheque\nNo.':
                        df.rename(columns = {"Ref No./Cheque\nNo.": "Ref.No"}, inplace = True)
                    elif col=='Txn No.':
                        df.rename(columns = {"Txn No.": "Ref.No"}, inplace = True)
                    elif col=='Tran Id':
                        df.rename(columns = {"Tran Id": "Ref.No"}, inplace = True)
                    elif col=='Debit':
                        pass
                    elif col=='Withdrawal Amt.':
                        df.rename(columns = {"Withdrawal Amt.": "Debit"}, inplace = True)
                    elif col=='Withdrawal Amount\n(INR)':
                        df.rename(columns = {"Withdrawal Amount\n(INR)": "Debit"}, inplace = True)
                    elif col=='Withdrawal Amount':
                        df.rename(columns = {"Withdrawal Amount": "Debit"}, inplace = True)
                    elif col=='Withdrawals':
                        df.rename(columns = {"Withdrawals": "Debit"}, inplace = True)
                    elif col=='Withdrawal':
                        df.rename(columns = {"Withdrawal": "Debit"}, inplace = True)
                    elif col=='Decrease':
                        df.rename(columns = {"Decrease": "Debit"}, inplace = True)
                    elif col=='Credit':
                        pass
                    elif col=='Deposit Amt.':
                        df.rename(columns = {"Deposit Amt.": "Credit"}, inplace = True)
                    elif col=='Deposit Amount\n(INR)':
                        df.rename(columns = {"Deposit Amount\n(INR)": "Debit"}, inplace = True)
                    elif col=='Deposit Amount':
                        df.rename(columns = {"Deposit Amount": "Credit"}, inplace = True)
                    elif col=='Deposit':
                        df.rename(columns = {"Deposit": "Credit"}, inplace = True)
                    elif col=='Deposits':
                        df.rename(columns = {"Deposits": "Credit"}, inplace = True)
                    elif col=='Increase':
                        df.rename(columns = {"Increase": "Credit"}, inplace = True)
                    elif col=='Date':
                        pass
                    elif col=='Tran Date':
                        df.rename(columns = {"Tran Date": "Date"}, inplace = True)
                    elif col=='Txn Date':
                        df.rename(columns = {"Txn Date": "Date"}, inplace = True)
                    elif col=='Transaction Date':
                        df.rename(columns = {"Transaction Date": "Date"}, inplace = True)
                    elif col=='Balance':
                        pass
                    elif col=='Closing Balance':
                        df.rename(columns = {"Closing Balance": "Balance"}, inplace = True)
                    elif col=='Closing Bal':
                        df.rename(columns = {"Closing Bal": "Balance"}, inplace = True)
                    elif col=='Closing Bal.':
                        df.rename(columns = {"Closing Bal.": "Balance"}, inplace = True)
                def rolling_group(val):
                    if pd.notnull(val): rolling_group.group +=1 
                    return rolling_group.group
                rolling_group.group = 0 
                def joinFunc(g,column):
                    col =g[column]
                    joiner = "/" if column == "Date" else ""
                    s = joiner.join([str(each) for each in col if pd.notnull(each)])
                    s = re.sub("(?<=&)"+joiner," ",s)
                    s = re.sub("(?<=-)"+joiner,"",s)
                    s = re.sub(joiner*2,joiner,s)   
                    return s
                groups = df.groupby(df['Date'].apply(rolling_group),as_index=False)
                groupFunct = lambda g: pd.Series([joinFunc(g,col) for col in g.columns],index=g.columns)
                x=groups.apply(groupFunct)
                x.to_csv('media/new.csv')
            df=pd.read_csv('media/new.csv',thousands=',')
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            df['Bank']=user_data['bankname']
            df.to_csv('media/output.csv')
#             os.remove('media/prevois/new.csv')
            os.remove('media/new.csv')
        return Response(user_data,status=status.HTTP_201_CREATED)

class NLPDataViews(generics.ListAPIView):
#     authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        list=[]
        qdata=ladgernamedata.objects.all()
        for q in qdata:
            list.append(str(q))
        df=pd.read_csv('media/output.csv')
        df = df.fillna({'Narration':'', 'Credit':0.00,'Debit':0.00}).fillna(0)
        df['Matched']=df['Narration']
        for d in df['Narration']:
            for l in list:
                if l in d:
                    df['Matched'] = df['Matched'].replace(d,l.upper())
                    break
            else:
                df['Matched'] = df['Matched'].replace(d,'')
        # header=['Date','Narration','Debit','Credit','Matched']
        df.to_csv('media/newoutput.csv')
        os.remove('media/output.csv')
        return Response(status=status.HTTP_200_OK)


class POSTDataView(generics.ListCreateAPIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class=ShowDataSerializer 
    def post(self, request, *args, **kwargs):
        try:  
            x=ShowData.objects.latest('id')
            dates=x.created_on
            q=EpaymentDetails.objects.latest('id')
            queryset = ShowData.objects.filter(bank=q)
            with open('media/newoutput.csv', 'r') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    row['Credit'] = row['Credit'].replace(',', '')
                    row['Debit'] = row['Debit'].replace(',', '')
                    model=ShowData.objects.create(
                            Date=row.get('Date',''),
                            Transaction=row.get('Narration',''),
                            Legder=row.get('Matched',''),
                            Ref_no=row.get('Ref.No',''),
                            Credit=row.get('Debit',''),
                            Debit=row.get('Credit',''),
                            )
                    model.prevoius_created_on=dates
                    model.save()
                    model1=EpaymentDetails.objects.latest('id')
                    print('hhhhhhh',model1)
                    model.bank=model1
                    model.save()
                list=[]
                for i in queryset.all():
                    list.append(str(i.Date))
                c=len(list)
                model2=EpaymentDetails.objects.filter(id=model1.id).update(s_date=list[0],e_date=list[-1],entry=c)
                print(model1.s_date)
                print(model2)
            x=str(q.file)
            file_extension = pathlib.Path(x).suffix
            print(file_extension)
            if file_extension=='.csv':
                headers=['Date','Narration','Debit','Credit','Balance']
                csv1 = pd.read_csv('media/newoutput.csv',usecols=headers)
                df = csv1.fillna("")
                df['Date'] = pd.to_datetime(df['Date'], dayfirst=True).dt.strftime('%d/%m/%Y')
                renamedata='CSVTOPDFDATA'+str(q.id)+'.pdf'

                df.to_html("media/demohtml/table.html")
                dest='media/pdf/'+renamedata
                print(dest)
                options = {'page-size': 'A4','margin-top': '0.75in','margin-right': '0.75in','margin-bottom': '0.75in','margin-left': '0.75in'}
                pdfkit.from_file("media/demohtml/table.html",dest,options=options)
                model2=EpaymentDetails.objects.filter(id=model1.id).update(file='pdf/'+renamedata)
            else:
                pass
#             os.remove('media/newoutput.csv')
        except ShowData.DoesNotExist:
            q=EpaymentDetails.objects.latest('id')
            queryset = ShowData.objects.filter(bank=q)
            with open('media/newoutput.csv', 'r') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    row['Credit'] = row['Credit'].replace(',', '')
                    row['Debit'] = row['Debit'].replace(',', '')
                    model=ShowData.objects.create(
                            Date=row.get('Date',''),
                            Transaction=row.get('Narration',''),
                            Legder=row.get('Matched',''),
                            Ref_no=row.get('Ref.No',''),
                            Credit=row.get('Debit',''),
                            Debit=row.get('Credit',''),
                            )
                    model.prevoius_created_on=model.created_on
                    model.save()
                    model1=EpaymentDetails.objects.latest('id')
                    print('hhhhhhh',model1)
                    model.bank=model1
                    model.save()
                list=[]
                for i in queryset.all():
                    list.append(str(i.Date))
                c=len(list)
                model2=EpaymentDetails.objects.filter(id=model1.id).update(s_date=list[0],e_date=list[-1],entry=c)
                print(model1.s_date)
                print(model2)
            x=str(q.file)
            file_extension = pathlib.Path(x).suffix
            print(file_extension)
            if file_extension=='.csv':
                headers=['Date','Narration','Debit','Credit','Balance']
                csv1 = pd.read_csv('media/newoutput.csv',usecols=headers)
                df = csv1.fillna("")
                df['Date'] = pd.to_datetime(df['Date'], dayfirst=True).dt.strftime('%d/%m/%Y')
                renamedata='CSVTOPDFDATA'+str(q.id)+'.pdf'

                df.to_html("media/demohtml/table.html")
                dest='media/pdf/'+renamedata
                print(dest)
                options = {'page-size': 'A4','margin-top': '0.75in','margin-right': '0.75in','margin-bottom': '0.75in','margin-left': '0.75in'}
                pdfkit.from_file("media/demohtml/table.html",dest,options=options)
                model2=EpaymentDetails.objects.filter(id=model1.id).update(file='pdf/'+renamedata)
            else:
                pass
#             os.remove('media/newoutput.csv')
        return Response(status=status.HTTP_201_CREATED)
    def get(self, request):
        q=EpaymentDetails.objects.latest('id')
        queryset = ShowData.objects.filter(bank=q)
        serializer = ShowDataSerializer(queryset,many=True)
        return Response(serializer.data)
class UpdateDeleteData(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class=ShowDataSerializer
    queryset = ShowData.objects.all()
    def get_object(self,pk):
        try:
            return ShowData.objects.get(id=pk)
        except ShowData.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def get(self, request,pk):
        queryset = self.get_object(pk)
        serializer = ShowDataSerializer(queryset)
        return Response(serializer.data)

    def patch(self, request,pk):  
        queryset = self.get_object(pk)
        serializer=self.serializer_class(data=request.data,many=True)
        if serializer.is_valid():
            queryset.Legder=request.data['Legder']
            queryset.ListAmount1=request.data['ListAmount1']
            queryset.ListLegder1=request.data['ListLegder1']
            queryset.ListAmount2=request.data['ListAmount2']
            queryset.ListLegder2=request.data['ListLegder2']
            queryset.EditLegder=request.data['EditLegder']
            queryset.EditLegder2=request.data['EditLegder2']
            queryset.EditLegderamount=request.data['EditLegderamount']
            queryset.EditLegder2amount=request.data['EditLegder2amount']
            queryset.Vouchetype=request.data['Vouchetype']
            queryset.Credit=request.data['Credit']
            queryset.Debit=request.data['Debit']
            queryset.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request,pk):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_200_OK)
class Newvoucherpost(generics.ListCreateAPIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class=ShowDataSerializer 
    def post(self, request, *args, **kwargs):
        q=EpaymentDetails.objects.latest('id')
        model=ShowData.objects.create(
                Date=request.POST.get('Date',''),
                Transaction=request.POST.get('Transaction',''),
                Legder=request.POST.get('Legder',''),
                Credit=request.POST.get('Credit',''),
                Debit=request.POST.get('Debit',''),
                EditLegder=request.POST.get('EditLegder',''),
                EditLegder2=request.POST.get('EditLegder2',''),
                ListLegder1=request.POST.get('ListLegder1',''),
                ListAmount1=request.POST.get('ListAmount1',''),
                ListLegder2=request.POST.get('ListLegder2',''),
                ListAmount2=request.POST.get('ListAmount2',''),
                Vouchetype=request.POST.get('Vouchetype',''),
                AccountantNarration=request.POST.get('AccountantNarration',''),
                )
        model.save()
        model1=EpaymentDetails.objects.latest('id')
        model.bank=model1
        model.save()
        return Response(status=status.HTTP_201_CREATED)


class Legderlist(views.APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class=LedgerDataSerializer
    def get(self, request, *args, **kwargs):
        login_user=request.user
#         queryset = ladgernamedata.objects.filter(created_by=login_user)
        queryset=ladgernamedata.objects.all()
        serializer=LedgerDataSerializer(queryset,many=True)
        return Response(serializer.data)

class ShowLegderlist(views.APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class=LedgerDataSerializer1
    def get(self, request, *args, **kwargs):
        login_user=request.user
        queryset = ladgernamedata.objects.all()
        serializer=LedgerDataSerializer1(queryset,many=True)
        return Response(serializer.data)

class ModelFilter(django_filters.FilterSet):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    bankname = django_filters.ModelChoiceFilter(queryset=BankDetails.objects.all())
    created_on=django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = EpaymentDetails
        fields = ['bankname','created_on']
class BankStatementfilter(generics.ListAPIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset=EpaymentDetails.objects.all()
    serializer_class=EpaymentSerializer1
    filter_backends1 = (DjangoFilterBackend)
    filterset_fields = ['bankname','created_on']    
    filter_class = ModelFilter
class Tallyaddbankvoucher(generics.ListAPIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        q=ShowData.objects.last()
        queryset = ShowData.objects.filter(created_on__gt=q.prevoius_created_on)
        serializer = ShowDataSerializer1(queryset,many=True)
        return Response(serializer.data)
      
