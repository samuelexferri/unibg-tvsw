"""pharmacies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from pharmacies import settings
from shop import views

schema_view = get_schema_view(
    openapi.Info(
        title="Pharmacies API",
        default_version='v0.1',
        description="Our API!",
        terms_of_service="https:/farmacie.pythonanywhere.com",
        contact=openapi.Contact(email="contact@farmacie.pythonanywhere.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  path('', views.homepage, name='home'),
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
                  url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  path('authentication/', include('authentication.urls')),
                  path('shop/', include('shop.urls')),
                  path('timetable/', include('timetable.urls')),
                  path('transfer/', include('transfer.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.sites.AdminSite.site_header = 'Pharmacies'
admin.sites.AdminSite.site_title = 'Pharmacies'
admin.sites.AdminSite.index_title = 'Admin'
