from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.dispatch import receiver,Signal
from django.db.models.signals import pre_save
from.models import sailary
from paidmodule.serializers import paidpaymentbanklist,FileUploadSerializer,Getsailarydata
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from e_checkapp.models import pp_path_m,PpPymntT,PpBnkM
from uuid import getnode as get_mac


class SnippetList(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = paidpaymentbanklist
    """
    List all snippets, or create a new snippet.
    """
    
    def get(self, request, format=None):
        login_uaer_data=request.user
        snippets = PpPymntT.objects.filter(usr=login_uaer_data)
        serializer = paidpaymentbanklist(snippets, many=True)
        return Response(serializer.data)

        
    def post(self, request, format=None):
        mysignal=Signal(providing_args=['name'])
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        mac = get_mac()
        serializer = paidpaymentbanklist(data=request.data)
        if serializer.is_valid(): 
            serializer.save(usr=self.request.user,entr_by=self.request.user,ip_addr=ip,mac_addr=mac)
            print("save sucefullllllllllllllll")
            mysignal.send(sender=PpPymntT,name='sunil')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

def index(request):
    return HttpResponse("<h1>MyClub Event Calendar</h1>")

from rest_framework import generics
from io import StringIO
import pickle
import csv
import os.path
import io  # Added

class sailarydata(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        login_user=request.user
        serializer_class = self.get_serializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        file = serializer_class.validated_data['file']
        decoded_file = file.read().decode()
        # upload_products_csv.delay(decoded_file, request.user.pk)
        io_string = io.StringIO(decoded_file)
        # reader = csv.reader(io_string)
        reader=csv.DictReader(io_string)
        print("GGGGGGGGGGGGg",reader)
        for row in reader: 
            print(row)
            model=sailary.objects.create(
                    uer=request.user,
                    Name=row.get('Name',''),
                    AMOUNT=row.get('AMOUNT',''), 
                  
                    )
            model.save()        
        return Response(status=status.HTTP_204_NO_CONTENT)
class getsailarydata(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Getsailarydata

    def get(self, request, format=None):
        login_uaer_data=request.user
        snippets = sailary.objects.filter(uer=login_uaer_data)
        serializer = Getsailarydata(snippets, many=True)
        return Response(serializer.data)    


