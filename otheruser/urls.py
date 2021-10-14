from django.urls import path
from . import views
from .views import*

urlpatterns = [
    path('otheruserregister/', OtheruserRegisterView.as_view(), name="otheruserregister"),#register new user
    path('otherusertokenvarification/', OtheruserVerifyEmail.as_view(), name="otherusertokenvarification"),# other user token varification
    path('otheruserlogin/', OtheruserLoginAPIView.as_view(), name="otheruserlogin"), # other user login 
    path('getalluserdata/', findadminuserdata.as_view(),
         name="getalluserdata"),  # other user login
    path('getallotheruserdata/<int:pk>/', OtheruserDetail.as_view(),
         name="getallotheruserdata")  # other user login
]




