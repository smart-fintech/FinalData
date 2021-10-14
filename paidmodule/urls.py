from django.urls import path
# from django.urls import path
from . import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from paidmodule import views




urlpatterns = [
    # path('emi/',PaidPaymet.as_view(), name='emi')
    path('snippets/', views.SnippetList.as_view()),
    path('getsailery/', views.getsailarydata.as_view()),
    path('sailaryupload/', views.sailarydata.as_view()),
    path('hhhh', views.index, name='index'),
]