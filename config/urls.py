from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ACCOUNT APP API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="contact@expenses.local"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('rest_framework.urls')),
    # path('api/', include('e_checkapp.urls')),
    # path('', include('posts.urls')),
    # path('test/', include('testapp.urls')),
    path('tally/', include('tallyapp.urls')),
    # path('payment/',include('pymentroll')),
    # path('paid/',include('paidmodule.urls')),
    path('otheruser/',include('otheruser.urls')),
    path('invoice/', include('invoice.urls')),
    path('e_payment/', include('e_payment.urls')),
    path('useraccount/', include('accountapp.urls')),
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),

    # path('api/api.json/', schema_view.without_ui(cache_timeout=0),
    #      name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
