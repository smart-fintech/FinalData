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
from xml.etree import ElementTree as Et
############################# django restframework start here  #################################
from tallyapp.models import ladgernamedata,voucherfromtally
from tallyapp.serializers import UpdateCompanySerializer, GetvoucherSerializer,ladegerSerializer,CompanySerializer,UpdateLegderSerializer,NormalCompanySerializer,PostladegerSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class VoucherPost(APIView):
    permission_classes = (IsAuthenticated,) 
    serializer_class = GetvoucherSerializer
    def get(self, request, format=None):
        snippets = voucherfromtally.objects.all()
        serializer = GetvoucherSerializer(snippets, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        print('doneeeee')
        return Response(status=status.HTTP_201_CREATED)

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
        login_user=request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save(created_by=login_user,ledeger_group='Capital Account')
        return Response(status=status.HTTP_201_CREATED)

class CompanyList(APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
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
        login_user=request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save(user_company=login_user)
        return Response(status=status.HTTP_201_CREATED)  

class NormalCompanyList(APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
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
  
