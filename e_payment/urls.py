from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('bankstmnt/',views.EpaymentDataPost.as_view()),
    path('NLPDataViews/',views.NLPDataViews.as_view()),
    path('PostViews/',views.POSTDataView.as_view()),
    path('UpdateDeleteData/<int:pk>/',views.UpdateDeleteData.as_view()),
    path('MasterbankViews/',views.MasterbankViews.as_view()),
    path('BankViews/',views.BankDetailsViews.as_view()),
    path('BankStatementfilter/', views.BankStatementfilter.as_view(), name='BankStatementfilter'),
    path('Legderlist/',views.Legderlist.as_view()),
    path('bankdata/',views.BankDetailsViews1.as_view()),
    path('newvoucher/',views.Newvoucherpost.as_view()),
    path('Tallyaddbankvoucher/',views.Tallyaddbankvoucher.as_view()),
    # path('new123/',views.new123),
]
