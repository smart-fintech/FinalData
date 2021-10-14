from django.urls import path

from .views import HomePageView,model_form_upload,printedcheckupdate # new
from . import views

urlpatterns = [
    path('home', HomePageView.as_view(), name='home'),
    path('assignbank', views.model_form_upload.as_view(), name='assignbank'),# create bank
    # path('addpayment', views.addpayment.as_view(), name='addpayment'),
    path('addprintedimage/<int:pk>/', views.printedcheckupdate.as_view(), name='addprintedimage'),#add printed image
]