
# from django.db.models import query
# from django.shortcuts import render,HttpResponse
# from rest_framework import generics, status,views,permissions,mixins
# from .models import PpOrgnM,PpPymntT,PpBnkM,masterBank,pp_path_m,pp_bankcrd_m,term_condition,BalancesheetData
# from datetime import datetime
# from .permistions import AccessPermission
# import decimal

# from django.http import HttpResponse, Http404

# from .serializers import (RegisterSerializer,
# EmailVerificationSerializer,
# LoginSerializer,
# ResetPasswordEmailRequestSerializer,
# SetNewPasswordSerializer,
# LogoutSerializer,
# PpBnkMSerializer,
# OrgSerializer,
# PpeSerializer,
# FileSerializer,
# PpPymntTSerializer,
# OrgListSerializer,
# BnkListSerializer,
# masterbankSerializer1,
# masterbanklistSerializer,
# termandconditionSerializer,
# BnkListSerializer,
# idnameSerializer,
# paymentbanklist,
# blankimgSerializer,
# paymentdsahSerializer,
# paymentdsahupdatestatusSerializer,
# blankchqprintscreenSerializer,
# BlankPictureSerialiser,
# UserRegisterSerializer,
# UserLoginSerializer,
# admingetotheruserdataserializer
# ,BalanceSheetSerializer)
# from rest_framework.generics import GenericAPIView
# from rest_framework.mixins import UpdateModelMixin
# import csv
# from django.conf import settings 
# from django.core.mail import send_mail
# from rest_framework.views import APIView

# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import User
# from .utils import Util
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
# import jwt
# from django.conf import settings
# from drf_yasg.utils import swagger_auto_schema
# from django.contrib.auth.tokens import PasswordResetTokenGenerator

# from drf_yasg import openapi
# from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
# # from .utils import Util
# from django.shortcuts import redirect
# from django.http import HttpResponsePermanentRedirect
# import os
# from rest_framework.views import APIView
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
# from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from rest_framework import filters
# from rest_framework.generics import ListAPIView
# from num2words import num2words
# from drf_multiple_model.views import ObjectMultipleModelAPIView
# from PIL import Image, ImageDraw, ImageFont
# from uuid import getnode as get_mac
# # class blankimage(APIView):
# from e_checkapp.models import pp_path_m,PpPymntT

# def num2words(num):
#     num = decimal.Decimal(num)
#     decimal_part = num - int(num)
#     num = int(num)
#     if decimal_part:
#         return num2words(num) + " point " + (" ".join(num2words(i) for i in str(decimal_part)[2:]))

#     under_20 = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
#     tens = ['Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
#     above_100 = {100: 'Hundred',1000:'Thousand', 100000:'Lakhs', 10000000:'Crores'}

#     if num < 20:
#        return under_20[num]

#     if num < 100:
#         return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10])

#     # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
#     pivot = max([key for key in above_100.keys() if key <= num])

#     return num2words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words(num%pivot))

# def getimagename(pk):
#     firstpost = PpPymntT.objects.get(pymnt_id=pk)
#     return firstpost.bnk_id.cover
   

# class CustomRedirect(HttpResponsePermanentRedirect):

#     allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']
# # for register new user
# # loging api
# class RegisterView(generics.GenericAPIView):
#     authentication_classes = (TokenAuthentication,)
#     serializer_class = RegisterSerializer

#     def post(self,request):
#         try:
#             email = request.data
#             serializer = self.serializer_class(data=email)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             user_data=serializer.data
#             # email=request.user_data['email']
#             # print("email email",email)
#             data=user_data['email']
#             print("8888",data)
#             user = User.objects.get(email=user_data['email'])
#             print("&&&&&&&&&&&777",user)
#             token = RefreshToken.for_user(user).access_token
#             current_site = get_current_site(request).domain
#             relativeLink = reverse('email-verify')
#             absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
#             email_body = 'Hi Use the link below to verify your email \n' + absurl   
#             data = {'email_body': email_body, 'to_email': user.email,
#                     'email_subject': 'Verify your email'}        
#             Util.send_email(data)
#             return Response(user_data,status=status.HTTP_201_CREATED)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")

# class UserRegisterView(generics.GenericAPIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UserRegisterSerializer
#     # renderer_classes = (UserRenderer,)
#     def post(self, request):
#         loginuser=request.user
#         email = request.data
#         print("HHHHHHHHHHHHHHHHHHh", loginuser)
#         serializer = self.serializer_class(data=email)

#         serializer.is_valid(raise_exception=True)
#         serializer.save(created_by=loginuser,is_staff=False)
#         user_data = serializer.data
#         # print(user_data)
#         user = User.objects.get(email=user_data['email'])
#         token = RefreshToken.for_user(user).access_token
#         current_site = get_current_site(request).domain
#         relativeLink = reverse('email-verify')
#         absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
#         email_body = 'Hi Use the link below to verify your email \n' + absurl

#         data = {'email_body': email_body, 'to_email': user.email,
#                 'email_subject': 'Verify your email'}

#         Util.send_email(data)
#         return Response(user_data, status=status.HTTP_201_CREATED)


# class UserLoginAPIView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         email = request.POST.get('email', '')
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#         # except Exception as e:
#         #    return HttpResponse("something get worn please cntect admin")    

# # for user email varification api
# class VerifyEmail(views.APIView):
#     serializer_class = EmailVerificationSerializer
#     token_param_config = openapi.Parameter(
#         'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
#     @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self, request):
#         token = request.GET.get('token')
#         print('44444444444444444444444444')
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY)
#             print(",$$$$$$$$$$$$$$$$$$$$$$$")
#             print('susssssssssssssssssssssss',payload)
#             user = User.objects.get(id=payload['user_id'])
#             print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^6")
#             if not user.is_verified:
#                 user.is_verified = True
#                 user.save()
#             return Response({'token':token,'email': 'Successfully activated'}, status=status.HTTP_200_OK)
#         except jwt.ExpiredSignatureError as identifier:
#             return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.DecodeError as identifier:
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
# # for user login api
# class LoginAPIView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         email = request.POST.get('email','')
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#         # try:
            
#         # except Exception as e:
#         #    return HttpResponse("something get worn please cntect admin")                        


# class findadminuserdata(views.APIView):
#     # authentication_classes = (TokenAuthentication,)
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = (AccessPermission,)
#     serializer_class = admingetotheruserdataserializer
#     def get(self, request, format=None):
#         try:
#             query=User.objects.all()
#             serializer = admingetotheruserdataserializer(query, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")    


# class BalanceSheetDetailsView(APIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = [IsAuthenticated, AccessPermission]
#     serializer_class = BalanceSheetSerializer

#     def get(self, request, *args, **kwargs):
#         try:
#             loginuser = request.user
#             query = BalancesheetData.objects.filter(created_by=loginuser)
#             serializer = BalanceSheetSerializer(query, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")

#     def post(self, request, format=None):
#         try:
#             serializer = BalanceSheetSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(created_by=self.request.user)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")    

# # for send token on mail
# class RequestPasswordResetEmail(generics.GenericAPIView):
#     serializer_class = ResetPasswordEmailRequestSerializer
#     def post(self, request):
#         try:
#             serializer = self.serializer_class(data=request.data)

#             email = request.data.get('email', '')

#             if User.objects.filter(email=email).exists():
#                 user = User.objects.get(email=email)
#                 uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#                 token = PasswordResetTokenGenerator().make_token(user)
#                 current_site = get_current_site(
#                     request=request).domain
#                 relativeLink = reverse(('email-verify'))
#                 absurl = 'http://'+current_site + relativeLink
#                 email_body = 'Hello,\n Use link below to reset your password  \n' + absurl
#                 # absurl='http://'+corrent_site+relativeLink
#                 data = {'email_body': email_body, 'to_email': user.email,
#                         'email_subject': 'Reset your passsword'}
#                 Util.send_email(data)
#             return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")
            

# #for genrate token for resetpassword
# class PasswordTokenCheckAPI(generics.GenericAPIView):
#     serializer_class = SetNewPasswordSerializer
#     def get(self, request, uidb64, token):

#         redirect_url = request.GET.get('redirect_url')

#         try:
#             id = smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)
#             # for i in user:
#             #     print("%%%%%%%%%%%%%%%%%%%%%55",i.id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 if len(redirect_url) > 3:
#                     return CustomRedirect(redirect_url+'?token_valid=False')
#                 else:
#                     return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

#             if redirect_url and len(redirect_url) > 3:
#                 return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
#             else:
#                 return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

#         except DjangoUnicodeDecodeError as identifier:
#             try:
#                 if not PasswordResetTokenGenerator().check_token(user):
#                     return CustomRedirect(redirect_url+'?token_valid=False')
                    
#             except UnboundLocalError as e:
#                 return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)



# # for enter new password by the user when user is login 
# class SetNewPasswordAPIView(generics.GenericAPIView):
#     serializer_class = SetNewPasswordSerializer

#     def patch(self, request):
#         try:
#             serializer = self.serializer_class(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
        
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")    

# # for logout api 
# class LogoutAPIView(generics.GenericAPIView):
#     serializer_class = LogoutSerializer

#     permission_classes = (permissions.IsAuthenticated,)
#     def post(self, request):
#         try:
#             serializer = self.serializer_class(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")

# # function for add  payment list    
# class PpBnkMAPIView(generics.GenericAPIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = PpBnkMSerializer
#     # renderer_classes = (UserRenderer,)
#     def post(self, request):
#         try:
#             user=request.user
#             email = request.data
#             print('$$$$$$$$$$$$$$$$$$',email)
#             serializer = self.serializer_class(data=email)
#             serializer.is_valid(raise_exception=True)
#             serializer.save(usr=self.request.user,entr_by=self.request.user)
#             return Response(status=status.HTTP_201_CREATED)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")     


# # function get all list and post data for oraganation
# class ppOrgSAPIView(APIView):
#     # authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,) 
#     serializer_class = OrgSerializer
#     def get(self, request, format=None):
#         login_uaer_data=request.user
#         snippets = PpOrgnM.objects.filter(usr=login_uaer_data)
#         serializer = OrgSerializer(snippets, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         mac = get_mac()
#         serializer = OrgSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(usr=self.request.user,entr_by=self.request.user,ip_addr=ip,mac_addr=mac)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# # function for update delete retrive oraganation
# class ppOrgSAPIViewDetail(APIView):
#     """
#     Retrieve, update or delete a org instance.
#     """
#     permission_classes = (IsAuthenticated,)
#     serializer_class = OrgSerializer
#     def get_object(self, pk):
#         try:
#             return PpOrgnM.objects.get(pk=pk)
#         except PpOrgnM.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = OrgSerializer(snippet)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         try:
#             snippet = self.get_object(pk)
#             serializer = OrgSerializer(snippet, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")     

#     def delete(self, request, pk, format=None):
#         try:  
#             snippet = self.get_object(pk)
#             snippet.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")     

# class ppeeAPIView(generics.GenericAPIView):
#     # authentication_classes = (SessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = PpeSerializer
#     # renderer_classes = (UserRenderer,)
#     def post(self, request):
#         try:
#             user=request.user
#             email = request.data
#             print('$$$$$$$$$$$$$$$$$$',email)
#             serializer = self.serializer_class(data=email)
#             serializer.is_valid(raise_exception=True)
#             serializer.save(usr=self.request.user,entr_by=self.request.user)
#             return Response(status=status.HTTP_201_CREATED)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")     

# # function for upload image
# class FileView(generics.GenericAPIView):
#     parser_classes = (MultiPartParser, FormParser)
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = FileSerializer      
#     def post(self, request, *args, **kwargs):
#         try:
#             obj = ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
#             file_serializer = FileSerializer(data=request.data,many=True)
#             if file_serializer.is_valid():
#                 file_serializer.save()
#                 return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")         
   
# class PaymentdataView(APIView):
#     # authentication_classes = (SessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = PpPymntTSerializer
#     # parser_classes = (MultiPartParser, FormParser)


#     def get(self, request, format=None):
#         try:
#             login_uaer_data=request.user
#             snippets = PpPymntT.objects.filter(usr=login_uaer_data)
#             serializer = PpPymntTSerializer(snippets, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")     
  
#     def post(self, request, format=None):
#         try:
#             x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#             if x_forwarded_for:
#                 ip = x_forwarded_for.split(',')[0]
#             else:
#                 ip = request.META.get('REMOTE_ADDR')
#             mac = get_mac()
#             serializer = PpPymntTSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(usr=self.request.user,entr_by=self.request.user,ip_addr=ip,mac_addr=mac,pymnt_sts='PP')
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")    



# class PaymentdataViewDetail(APIView):
#     """
#     Retrieve, update or delete a payment instance.
#     """
#     # authentication_classes = (SessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = PpPymntTSerializer
#     def get_object(self, pk):
#         try:
#             return PpPymntT.objects.get(pk=pk)
#         except PpPymntT.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None,*args, **kwargs):
#         snippet = self.get_object(pk)
#         serializer = PpPymntTSerializer(snippet)
#         PpPymntT.objects.filter(pymnt_id=snippet.pymnt_id).update(pymnt_sts="CM")
#         imagedata=pp_path_m.objects.get(path_id=1)
#         # get blank image path
#         imgdata=imagedata.path_img_nm.url
#         removeslace=imgdata
#         removeslace=imgdata[1:]
#         #open blank image
#         # image=Image.open((settings.MEDIA_ROOTremoveslace))

#         image = Image.open(settings.MEDIA_ROOT +'/Blank Cheque templet.png')
#         # /home/user5/Desktop/ml_apisetup/2nd_API/media/Blank Cheque templet.png

#         draw = ImageDraw.Draw(image)
#         font = ImageFont.truetype(settings.MEDIA_ROOT +'/ARIAL.TTF', size=50)
        
#         loginuser=request.user
#         imgpatg=[]
        
#         print('%%%%%%%%%%%%%%%%%%%%%%%%%55',loginuser)
#         #get lohin user check images
                
#         #schedule_entries = schedulesdb.objects.filter(user=request.user)
#         imagename = (str(getimagename(pk)).split("/")[1]).split(".")[0]   
#         with open(settings.MEDIA_ROOT +'/CSV/'+imagename+'.csv', 'r') as file:
          
#             csv_file = csv.DictReader(file)
#             for row1 in csv_file:
#                 if row1['label'] == "rupee_w2":
#                     h = int(row1['x1'])
#                     w = int(row1['y1'])
#                     (new_x, new_y) = (h,w)                                 
#         with open(settings.MEDIA_ROOT +'/CSV/'+imagename+'.csv', 'r') as file:
#             csv_file = csv.DictReader(file)
#             for row in csv_file:
#                 finaldata=[]
#                 # paymentdata=PpPymntT.objects.all()
#                 paymentdata = self.get_object(pk)

#                 # serializer = masterbankSerializer(snippet)
#                 # return Response(serializer.data)
#                 if row['label'] == "rupee_w1":
#                     h = int(row['x1'])
#                     w = int(row['y1'])
#                     (x, y) = (h+150,w+5)
#                     print("xxxxxxxxxxxxxxxxxxxxxxxxxxxx", x)   
#                 #payee means customer
#                     num =(paymentdata.pymnt_chq_amt)
#                     #pass function to convert amount from number to words including after decimal point
#                     data=num2words(num)
#                     Payee = data
#                     star  = "**"
#                     only="only"
#                     space=" "
#                     payee1 = star + Payee +space  +only + star 
#                     Payee2 = payee1.title()
#                     color = 'rgb(0, 0, 0)' # black color
#                     N = 55
#                     add_string = "-"
#                     if len(Payee) > 55:
#                         res = Payee[ : N] + add_string + Payee[N : ] 
#                         u = res.split("-")
#                         pri=(u[0]+'-')
#                         draw.text((x+150, y), pri, fill=color, font=font)
#                         draw.text((new_x+150, new_y), u[1], fill=color, font=font)
#                     else:
#                         draw.text((x+150, y), Payee2, fill=color, font=font)                   
#                     # print("h")


#                 elif row['label'] == "date":

#                     h = int(row['x1'])
#                     w = int(row['y1'])
#                 # (x, y) = (h-20,w+20)
#                     (x, y) = (h+100,w+10)
                        
#                     Payee = str(paymentdata.pymnt_chq_dt)
#                     # payee1=str(Payee.day,Payee.month,Payee.year)
#                     datetimeobject = datetime.strptime(Payee,'%Y-%m-%d')
#                     Payee = datetimeobject.strftime('%d%m%Y')
#                     print("%%%%%%%%%%%%%%%%%%%555",Payee)

        
#                     new_Payee=Payee.replace("", "  ")[1: -1]
#                     color = 'rgb(0, 0, 0)' # black color
#                     draw.text((x, y), new_Payee, fill=color, font=font)
#                     ##### payee name #######
#                 elif row['label'] == "payee":
#                     print("GFFFFFFFHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHhh")
#                     Payee = str(paymentdata.pymnt_nm)
#                     Payee1 = Payee.title()
#                     star = "**"
#                     payee2 = star +Payee1+star 
#                     val_height = round(int(row['x2'])-int(row['x1'])/2)
#                     val_width = round(int(row['y2'])-int(row['y1'])/2)
#                     (W, H) = (val_height,val_width+200)
                  
#                     w, h = draw.textsize(Payee)
                    
#                     color = 'rgb(0, 0, 0)' # black color
#                     draw.text(((W-w)/2,(H-h)/1.75),payee2, fill=color, font=font)

#                     ##### payee name #######

#                 elif row['label'] == "rupee_n":
#                     h = int(row['x1'])
#                     w = int(row['y1'])
            
#                     (x, y) = (h+150,w)
#                     Payee =str(paymentdata.pymnt_chq_amt)
#                     star = "**"
#                     payee1 = star + Payee + star 
#                     color = 'rgb(0, 0, 0)' # black color
#                     draw.text((x, y), payee1, fill=color, font=font)

#                 # image.save('/home/dds/Documents/cheque_printing/printer/citi5445.png', dpi=image.info['dpi'])
#                 imagedata=pp_path_m.objects.get(path_id=1)
#                 image.save(settings.MEDIA_ROOT +'/blankImg/Blank_Cheque_templet.png',dpi=image.info['dpi'])
#                 imagedata=pp_path_m.objects.get(path_id=1)
#                 # get blank image path
#                 imgdata=imagedata.path_img_nm.url
#                 data=1000100
      
        
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         try:
#             snippet = self.get_object(pk)
#             serializer = PpPymntTSerializer(snippet, data=request.data)
#             if serializer.is_valid():
#                 serializer.save(pymnt_sts="CM")
            
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")     

#     def delete(self, request, pk, format=None):
#         try:
#             snippet = self.get_object(pk)
#             snippet.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")     

    
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.generics import ListAPIView
# from rest_framework import viewsets

# class paymentList(APIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = [IsAuthenticated]
#     serializer_class=paymentbanklist
    
#     def get(self, request, format=None):
#         try:
#             login_uaer_data=request.user.id
#             data = PpPymntT.objects.filter(usr=login_uaer_data)
#             serializer = paymentbanklist(data, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")     


# class Showimg(APIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = [IsAuthenticated]
#     serializer_class = paymentbanklist
#     parser_classes = (MultiPartParser, FormParser)
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return PpPymntT.objects.get(pk=pk)
#         except PpPymntT.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         try:
#             snippet = self.get_object(pk)
#             serializer = paymentbanklist(snippet)
#             return Response(serializer.data)
#         except Exception as e:
#             return HttpResponse("something get worn please cntect admin")    


# from rest_framework import viewsets
# class paymentupdate(viewsets.ViewSet):
#     # authentication_classes = (SessionAuthentication,)
#     permission_classes = [IsAuthenticated]
#     def update(self,request,pk):
#         try:
#             pm=PpPymntT.objects.get(pymnt_id=pk)
#             ps=PpPymntTSerializer(pm,request.data,partial=True)
#             print(ps)
#             if ps.is_valid():
#                 ps.save()
#                 return Response({"message":"Update successfuylly"})
#             else:
#                 return Response({"error":ps.errors})
#         except PpPymntT.DoesNotExist:
#             return Response({"error":"Invalid"})





# # function for send mail
# class senddetail(APIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = PpPymntTSerializer
#     """
#     Retrieve, data only for id.
#     """
#     def get_object(self, pk):
#         try:
#             return PpPymntT.objects.get(pk=pk)
#         except PpPymntT.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):

#         snippet = self.get_object(pk)
#         email_from=request.user.email
#         recipient_list=[snippet.message_to]
#         payee_name=snippet.pymnt_nm
#         orgn_name=snippet.orgn
#         accoun_number=snippet.pymnt_ac_no
#         pymnt_data=snippet.pymnt_chq_dt
#         check_number=snippet.pymnt_chq_no
#         check_amount=snippet.pymnt_chq_amt
#         subject = 'welcome to e_check world'
#         message = "please check your detail ".join([payee_name, accoun_number,check_number,str(check_amount)]) 
#         send_mail( subject, message, email_from, recipient_list ) 
#         serializer = PpPymntTSerializer(snippet)
#         return Response(serializer.data)

# from django.http import HttpResponse
# # function for genreate csv
# def csvfilegenreate(request,pk):
#     response = HttpResponse(content_type='text/csv')
#     writer=csv.writer(response)
#     writer.writerow(['Payee Name','Account No','Cheque Date','Cheque No','Cheque Amount'])
#     data1=PpPymntT.objects.filter(pk=pk).values_list('pymnt_nm','pymnt_ac_no','pymnt_chq_dt','PYMENT_CHQ_NO','pymnt_chq_amt')
#     print('###########33333',data1)
#     # data2=data1.pppymntt_set.all().
#     for dada in data1:
#         print("csav###########################",dada)
#         writer.writerow(dada)
#         data2=csv
#         response['Content-Disposition']='attachment; filename=detail.csv'
#     return response 

# # function for filter data on check
# class Checkfilter(ListAPIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset=PpPymntT.objects.all()
#     serializer_class=PpPymntTSerializer
#     search_fields = ['pymnt_nm','pymnt_chq_amt']
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     filterset_fields = {
#     'pymnt_chq_dt':['gte', 'lte', 'exact', 'gt', 'lt'],
    
# }
#     def get_queryset(self):
#         user=self.request.user
#         return PpPymntT.objects.filter(usr=user)    

# # function for login orgaganation list login user
# class OrgList(APIView):
#     """
#     List all login user  organation,.
#     """
#     # authentication_classes = (SessionAuthentication,)
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrgListSerializer
#     def get(self, request, format=None):
        
#         login_uaer_data=request.user
#         # schedule_entries = PpOrgnM.objects.filter(usr=login_uaer_data)
#         snippets = PpOrgnM.objects.filter(usr_id=self.request.user)
#         serializer = OrgListSerializer(snippets, many=True)
#         return Response(serializer.data)
    

# class BnkList(APIView):
#     """
#     List all login  organation,.
#     """
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = [IsAuthenticated]
#     serializer_class = BnkListSerializer
#     def get(self, request, format=None):
#         try:
#             login_uaer_data=request.user
#             # schedule_entries = PpOrgnM.objects.filter(usr=login_uaer_data)
#             snippets = PpBnkM.objects.filter(usr_id=self.request.user)
#             serializer = BnkListSerializer(snippets, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")     

# # class Savebnk(generics.ListCreateAPIView):
# #     queryset = PpBnkM.objects.all()
# #     serializer_class = masterbankSerializer
# # class Savebnklist(APIView):
# #     authentication_classes = (SessionAuthentication,)
# #     permission_classes = [IsAuthenticated]
# #     serializer_class = masterbankSerializer
# #     def get(self, request, format=None):
# #         snippets = PpBnkM.objects.filter(usr_id=self.request.user)
# #         serializer = masterbankSerializer(snippets, many=True)
# #         return Response(serializer.data)

# #     def post(self, request, format=None):
# #         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
# #         if x_forwarded_for:
# #             ip = x_forwarded_for.split(',')[0]
# #         else:
# #             ip = request.META.get('REMOTE_ADDR')
# #         mac = get_mac()
# #         serializer = masterbankSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save(usr=self.request.user,entr_by=self.request.user,ip_addr=ip,mac_addr=mac)
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # function for save bank data 
# class SavebnkDetail(APIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = [IsAuthenticated]
#     serializer_class = masterbankSerializer1
#     parser_classes = (MultiPartParser, FormParser)
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return PpBnkM.objects.get(pk=pk)
#         except PpBnkM.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         try:
#             snippet = self.get_object(pk)
#             serializer = masterbankSerializer1(snippet)
#             return Response(serializer.data)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")     

#     def put(self, request, pk, format=None,partial=True):
#         try:
#             snippet = self.get_object(pk)
#             serializer = masterbankSerializer1(snippet, data=request.data)
#             if serializer.is_valid():
#                 cover=request.data.get('cover','')
#                 serializer.save(cover=cover)
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")         

        

#     def delete(self, request, pk, format=None):
#         try:
#             snippet = self.get_object(pk)
#             snippet.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")         


# from rest_framework.generics import GenericAPIView
# from rest_framework.mixins import UpdateModelMixin
# from rest_framework.viewsets import ModelViewSet
# from rest_framework import serializers




# # function for show all master list
# class mstrbnklist(APIView):
#     """
#     List all login  organation,.
#     """
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = [IsAuthenticated]
#     # serializer_class = BnkListSerializer
#     def get(self, request, format=None):
#         try:
#             login_uaer_data=request.user
#             # schedule_entries = PpOrgnM.objects.filter(usr=login_uaer_data)
#             snippets = masterBank.objects.all()
#             serializer = masterbanklistSerializer(snippets, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")          


# # function for get data id with name

# class idnamebnklist(APIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = [IsAuthenticated]
#     serializer_class = idnameSerializer
#     def get(self, request, format=None):
#         try:
#             snippets = PpBnkM.objects.filter(usr_id=self.request.user)
#             serializer = idnameSerializer(snippets, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")         


# # import csv
# # from django.http import HttpResponse
# # import os
# # def csv_upload(request):
# #     filefolder = settings.MEDIA_ROOT + '/inference/'
# #     os.chdir(filefolder)
# #     with open(filefolder+'.csv') as csvfile:
# #         reader = csv.DictReader(csvfile)
# #         for row in reader:
# #             p = Post(label=row['label'], x1=row['x1'],y1=row['y1'],x2=row['x2'],y2=row['y2'])
# #             p.save()

# #     # data=Post.objects.all()
# #     # print("^^^^^^^^^^^^^^^^^^^^^^^^^",data)
# #     return HttpResponse("get data sucefully")
 

# class Termandcondition(APIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = [IsAuthenticated]
#     serializer_class = termandconditionSerializer
#     def get(self, request, format=None):
#         snippets = term_condition.objects.all()
#         serializer = termandconditionSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         mac = get_mac()
#         serializer = termandconditionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(created_by=self.request.user,ip_addr=ip,mac_addr=mac,is_activate=True)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# #get all print completed payment list on payment list
# class getpaymentdashbord(APIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = [IsAuthenticated]
#     serializer_class = paymentdsahSerializer
#     def get(self, request, format=None):
#         try:
#             login_user=request.user
#             snippets = PpPymntT.objects.all().filter(pymnt_sts='CM',usr=login_user,paymentactive_status='0')
#             print("@@@@@@@@@@@@@@@",snippets)
#             serializer = paymentdsahSerializer(snippets, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")         

# # function for checkvarification
# class check_varification(APIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = paymentdsahupdatestatusSerializer
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, pk, format=None):
#         try:
#             snippet = self.get_object(pk)
#             serializer = paymentdsahupdatestatusSerializer(snippet)
#             return Response(serializer.data)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")         

#     def get_object(self, pk):
#         try:
#             return PpPymntT.objects.get(pk=pk)
#         except PpPymntT.DoesNotExist:
#             raise Http404

#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = paymentdsahupdatestatusSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user,paymentactive_status='1')
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# #get all payment list on blanck check print screen
# class getprintpending(APIView):

#     authentication_classes = (SessionAuthentication,)
#     permission_classes = [IsAuthenticated]
#     serializer_class = blankchqprintscreenSerializer
#     def get(self, request, format=None):
#         try:
#             login_user=request.user
#             snippets = PpPymntT.objects.filter(pymnt_sts='PP',usr=login_user)
#             print("@@@@@@@@@@@@@@@",snippets)
#             serializer = blankchqprintscreenSerializer(snippets, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#            return HttpResponse("something get worn please cntect admin")         

# # api for get blank img
# class getbalnkimg(APIView):
#     def get(self, request):
#         '''
#         Get Image
#         '''
#         try:
#             picture =pp_path_m.objects.get(path_id=1)
#         except pp_path_m.DoesNotExist:
#             raise Http404
#         serialiser = BlankPictureSerialiser(picture)
#         return Response(serialiser.data)

# # from django.http import HttpResponse
# # from .resources import PersonResource
# # from tablib import Dataset
# # from .models import Person
# # class getbalnkimg(APIView):
# #     def simple_upload(request):
    
# #         person_resource = PersonResource()
# #         dataset = Dataset()
# #         new_persons = request.FILES['myfile']
# #         imported_data = dataset.load(new_persons.read(),format='xlsx')
# #         #print(imported_data)
# #         for data in imported_data: path('getprintedimg/<int:pk>/', Showimg.as_view(), name="bankdata"),
# #             print(data[1])
# #             value = Person(
# #             data[0],
# #             data[1],
# #             data[2],
# #             data[3]
# #             )
# #             value.save()
# #         #result = person_resource.import_data(dataset, dry_run=True) # Test the data import
# #         #if not result.has_errors():
# #         # person_resource.import_data(dataset, dry_run=False) # Actually import now
# #         return render(request, 'input.html')
