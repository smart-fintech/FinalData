from django.urls import path
from . import views
from .views import (RegisterView,
VerifyEmail,
LoginAPIView,
RequestPasswordResetEmail,
PasswordTokenCheckAPI,
SetNewPasswordAPIView,
LogoutAPIView,
PpBnkMAPIView,
ppOrgSAPIView,
ppeeAPIView,
FileView,
PaymentdataView,
check_varification,
senddetail,
csvfilegenreate,
Checkfilter,
paymentList,
paymentupdate,
ppOrgSAPIViewDetail,
PaymentdataViewDetail,
OrgList,
BnkList,
# Savebnklist,
SavebnkDetail,
mstrbnklist,
idnamebnklist,
Termandcondition,
getpaymentdashbord,
getprintpending,
getbalnkimg,
Showimg,
UserRegisterView,
UserLoginAPIView,
findadminuserdata ,  # blankimage,
                    BalanceSheetDetailsView

)
from e_checkapp import views
from rest_framework_simplejwt.views import TokenRefreshView
   


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),#register new user
    path('login/', LoginAPIView.as_view(), name="login"),#login user
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),#regresh token
    path('userregister/', UserRegisterView.as_view(), name="userregister"),#useregister
    path('userlogin/', UserLoginAPIView.as_view(), name="userlogin"),  # userlogin
    path('getalluserdata/', findadminuserdata.as_view(),
         name="getalluserdata"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),#logout user
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),#varify email
    path('org/', ppOrgSAPIView.as_view(), name="org"),#create orgation
    path('org/<int:pk>/', views.ppOrgSAPIViewDetail.as_view()),#get,put,delet orgation by list
    path('pee/', ppeeAPIView.as_view(), name="pee"),#get paydata
    path('fileupload/', FileView.as_view(), name='fileupload'),#upload simple file
    path('orglist/', OrgList.as_view(), name='orglist'),#get login user own orgation list
    path('bnklist/', BnkList.as_view(), name='bnklist'),#getlogin user own oragation list
    path('alldata/', idnamebnklist.as_view(), name='alldata'),#get all master bank data
    path('getallpymentdashbord/', getpaymentdashbord.as_view(), name='getallpymentdashbord'),#get all payment list on payment dashbord data
    path('getallpaymentlist/', getprintpending.as_view(), name='getallpaymentlist'),#get all payment list on blanck chq printing screen dashbord data
#     path('savebank/', Savebnklist.as_view(), name='savebank'),
    path('termandcondition/', Termandcondition.as_view(), name='termandcondition'),#ter and condition
    path('getblankimg/', getbalnkimg.as_view(), name='getblankimg'),# get blank image api
    path('savebank/<int:pk>/', SavebnkDetail.as_view(), name='savebank'),# create bank
    path('mstbnklist/', mstrbnklist.as_view(), name='mstbnklist'),#get all master bank
#     path('blankimage/<int:pk>/', blankimage.as_view(), name='blankimage'),

    path('payment/', PaymentdataView.as_view(), name='payment'),# create payment
    path('payment/<int:pk>/', PaymentdataViewDetail.as_view(), name='payment'),#get,put,delete payment by id
    path('checkverify/<int:pk>/', check_varification.as_view(), name='checkverify'),#check varification
    path('sendmail/<int:pk>/', views.senddetail.as_view(),name='sendmail'),#send mail
    path('genreatecsv/<int:pk>/', views.csvfilegenreate,name='genreatecsv'),#genreate csv
    path('filterdata/', Checkfilter.as_view(), name='filterdata'),#filter pyament data
    path('pyamentlist/', paymentList.as_view(), name='pyamentlist'),#get all login user own payment list
    path('paymentupdate/<int:pk>/',views.paymentupdate.as_view({"put":"update"}), name='paymentupdate'),#get ,put,delet,payment by id

    path('request-reset-email/', RequestPasswordResetEmail.as_view(),#end mail for reset password
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),#getnreate new token
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),#password reset complet
         name='password-reset-complet'),
    path('bankdata/', PpBnkMAPIView.as_view(), name="bankdata"),#get all login user  bank data
    path('getprintedimg/<int:pk>/', Showimg.as_view(), name="bankdata"),#get all login user  bank data
    path('balancesheet/', BalanceSheetDetailsView.as_view(), name="balancesheet")
   
#     path('getdata', views.csv_upload,name='getdata')    
]
