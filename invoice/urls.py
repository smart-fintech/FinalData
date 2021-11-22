from django.urls import path
from .views import Buyerdataeditdelete,Invoicetotal, PaymentVouchereditdelete,PaymentVoucherentry,InvoiceOtherdata,MainInvoiceShow,UpdateHsndetails, Voucherentry,CreateInvoicefilter, BuyerDetailsView, SellerDetailsView, InvoiceDetailsView, InvoiceDataView,CsvInvoicedataAPI,GetcsvInvoicedataAPI,UploadCSVView,UpdatecsvDataAPI,NewMainInvoiceShow,LegderShow,CompanyShow,Sellerdataeditdelete,Invoiceeeditdelete,Invoicedataeeditdelete,ReceiptReportViews,ReceiptInvoicefilter

urlpatterns = [
    path('receiptinvoice/', ReceiptReportViews.as_view(), name='receiptinvoice'),
    path('createinvoicereport/', CreateInvoicefilter.as_view(), name='createinvoicereport'),
    path('receiptinvoicereport/', ReceiptInvoicefilter.as_view(), name='receiptinvoicereport'),
    path('legdershow/', LegderShow.as_view(), name='legdershow'),
    path('companyshow/', CompanyShow.as_view(), name='companyshow'),
    path('buyerdata/', BuyerDetailsView.as_view(), name='buyerdata'),
    path('sellerdata/', SellerDetailsView.as_view(), name='sellerdata'),
    path('invoice/', InvoiceDetailsView.as_view(), name='invoice'),
    path('invoicedata/', InvoiceDataView.as_view(), name='invoicedata'),
    path('csvinvoice/',CsvInvoicedataAPI.as_view(), name='csvinvoice'),
    path('getcsvinvoice/',GetcsvInvoicedataAPI.as_view(), name='getcsvinvoice'),
    path('maininvoice/', MainInvoiceShow.as_view(), name='maininvoice'),
    path('UploadCSVView/', UploadCSVView.as_view(), name='UploadCSVView'),
    path('UpdateHsndetails/<int:pk>/',UpdateHsndetails.as_view(),name='UpdateHsndetails'),
    path('UpdatecsvDataAPI/<int:pk>/',UpdatecsvDataAPI.as_view(),name='UpdatecsvDataAPI'),
    path('NewMainInvoiceShow/', NewMainInvoiceShow.as_view(), name='NewMainInvoiceShow'),
    path('buyeredit/<int:pk>/', Buyerdataeditdelete.as_view(), name='buyeredit'),
    path('selleredit/<int:pk>/',Sellerdataeditdelete.as_view(), name='selleredit'),
    path('invoiceedit/<int:pk>/',Invoiceeeditdelete.as_view(), name='invoiceedit'),
    path('invoicedataedit/<int:pk>/',Invoicedataeeditdelete.as_view(), name='invoicedataedit'),
    path('voucherinvoice/', Voucherentry.as_view(), name='voucherinvoice'),
    path('PaymentVoucherentry/', PaymentVoucherentry.as_view(), name='PaymentVoucherentry'),
    path('PaymentVouchereditdelete/<int:pk>/', PaymentVouchereditdelete.as_view(), name='PaymentVouchereditdelete'),
    path('Invoicetotal/', Invoicetotal.as_view(), name='Invoicetotal'),
    path('InvoiceOtherdata/', InvoiceOtherdata.as_view(), name='InvoiceOtherdata')
    # path('getpdf/', getpdf, name='getpdf'),
    
]
