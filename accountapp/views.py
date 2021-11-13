from django.shortcuts import render
from .serializers import (RegisterSerializer,
EmailVerificationSerializer,
LoginSerializer,
ResetPasswordEmailRequestSerializer,
SetNewPasswordSerializer,
LogoutSerializer,
UserRegisterSerializer,
UserLoginSerializer,
admingetotheruserdataserializer,
Updateuserserializer,
)
from django.shortcuts import render,HttpResponse
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import GenericAPIView

from rest_framework import generics, status,views,permissions,mixins

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
import csv
from django.conf import settings 
from django.core.mail import send_mail
from rest_framework.views import APIView

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
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
# Create your views here.
class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']
# for register new user
# loging api
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):   
        email = request.data
        serializer = self.serializer_class(data=email)
        serializer.is_valid()
        serializer.save()
        user_data=serializer.data
        # email=request.user_data['email']
        # print("email email",email)
        data=user_data['email']
        print("8888",data)
        user = User.objects.get(email=user_data['email'])
        print("&&&&&&&&&&&777",user)
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi Use the link below to verify your email \n' + absurl   
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}        
        Util.send_email(data)
        return Response(user_data,status=status.HTTP_201_CREATED)
        # except Exception as e:
        #    return HttpResponse("something get worn please cntect admin")

class UserRegisterView(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)   
    serializer_class = UserRegisterSerializer
    # renderer_classes = (UserRenderer,)
    def post(self, request):
        loginuser=request.user
        email = request.data
        print("HHHHHHHHHHHHHHHHHHh", loginuser)
        serializer = self.serializer_class(data=email)

        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=loginuser,is_staff=False)
        user_data = serializer.data
        # print(user_data)
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi Use the link below to verify your email \n' + absurl

        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
        # except Exception as e:
        #    return HttpResponse("something get worn please cntect admin")    

# for user email varification api
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
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
            user = User.objects.get(id=payload['user_id'])
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^6")
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'token':token,'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
# for user login api
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        email = request.POST.get('email','')
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # try:
            
        # except Exception as e:
        #    return HttpResponse("something get worn please cntect admin")                        


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
        
        except Exception as e:
           return HttpResponse("something get worn please cntect admin")    

# for logout api 
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
           return HttpResponse("something get worn please cntect admin")


class findadminuserdata(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = admingetotheruserdataserializer
    def get(self, request, format=None):
        try:
            login_user=request.user
            query=User.objects.filter(created_by=login_user)
            serializer = admingetotheruserdataserializer(query, many=True)
            return Response(serializer.data)
        except Exception as e:
           return HttpResponse("something get worn please cntect admin")    

class UpdateUser(APIView):
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = Updateuserserializer(snippet)
        return Response(serializer.data)
    
    def patch(self, request,pk, *args, **kwargs):
        snippet = self.get_object(pk)
        serializer = Updateuserserializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

