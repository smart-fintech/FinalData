from django.urls import path
from tallyapp import views
from .views import ladegerList

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('postlegder/', views.LegderPost.as_view()),
    path('postvoucher/', views.VoucherPost.as_view()),
    path('api/fetchladeger/', views.ladegerList.as_view()),
    path('getcompanynamedetails/', views.CompanyList.as_view()),
    path('getcompanydetails/', views.NormalCompanyList.as_view()),
    path('UpdateCompany/<int:pk>/', views.UpdateCompany.as_view()),
    path('UpdateLegder/<int:pk>/', views.UpdateLegder.as_view()),
]
