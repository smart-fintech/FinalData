from django.urls import path
from . import views
from .views import (RegisterView,
VerifyEmail,
LoginAPIView,
UserRegisterView,
UserLoginAPIView,
LogoutAPIView,
LogoutAPIView,
PortAPI,
)
from e_checkapp import views
from rest_framework_simplejwt.views import TokenRefreshView
   


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),#register new user
    path('login/', LoginAPIView.as_view(), name="login"),#login user
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),#regresh token
    path('userregister/', UserRegisterView.as_view(), name="userregister"),#useregister
    path('userlogin/', UserLoginAPIView.as_view(), name="userlogin"),  # userlogin
    path('logout/', LogoutAPIView.as_view(), name="logout"),#logout user
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),#varify email
    path('portpost/', PortAPI.as_view(), name="portpost"),
]
