from django.shortcuts import render
from .models import Otheruser
from .serializers import (OtheruserRegisterSerializer, OtheruserEmailVerificationSerializer,
                          Otheruserloginserializer, admingetotheruserdataserializer)
# from .serializers import 
from rest_framework import generics, status,views,permissions,mixins
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
import csv
from django.conf import settings 
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from e_checkapp .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from drf_yasg import openapi
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# from .utils import Util
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListAPIView
from num2words import num2words
from PIL import Image, ImageDraw, ImageFont
from uuid import getnode as get_mac
# Create your views here.


class OtheruserRegisterView(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = OtheruserRegisterSerializer
    # renderer_classes = (UserRenderer,)
    def post(self, request):
        email = request.data
        login_user=request.user
        serializer = self.serializer_class(data=email)
       
        serializer.is_valid(raise_exception=True)
        serializer.save(Otheruser_name=login_user)
        user_data=serializer.data
        print(user_data)
        user = Otheruser.objects.get(Otheruser_email=user_data['Otheruser_email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi Use the link below to verify your email \n' + absurl
            
        data = {'email_body': email_body, 'to_email': user.Otheruser_email,
                'email_subject': 'Verify your email'}
                
        Util.send_email(data)
        print("%%%%%%%%%%%%%%%5",data)
        return Response(user_data,status=status.HTTP_201_CREATED)


class OtheruserVerifyEmail(views.APIView):
    serializer_class = OtheruserEmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        print('44444444444444444444444444')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            print(",$$$$$$$$$$$$$$$$$$$$$$$")
            print('susssssssssssssssssssssss',payload)
            user = Otheruser.objects.get(id=payload['id'])
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^6")
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'token':token,'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class OtheruserLoginAPIView(generics.GenericAPIView):
    serializer_class = Otheruserloginserializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class findadminuserdata(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = admingetotheruserdataserializer

    def get(self, request, format=None):
        login_uaer_data = request.user
        snippets = Otheruser.objects.filter(Otheruser_name=login_uaer_data)
        serializer = admingetotheruserdataserializer(snippets, many=True)
        return Response(serializer.data)


class OtheruserDetail(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = admingetotheruserdataserializer
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Otheruser.objects.get(pk=pk)
        except Otheruser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = admingetotheruserdataserializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = admingetotheruserdataserializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Otherusercustom_permition(APIView):
    authentication_classes = (SessionAuthentication,)
   
    serializer_class = admingetotheruserdataserializer

    def get_object(self, pk):
        try:
            return Otheruser.objects.get(pk=pk)
        except Otheruser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = admingetotheruserdataserializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = admingetotheruserdataserializer(
            snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

