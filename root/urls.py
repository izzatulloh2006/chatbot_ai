from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def home (request):
    return  HttpResponse("Helcome to home page")

urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/v1/', include('apps.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', home, name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


