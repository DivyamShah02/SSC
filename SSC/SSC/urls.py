from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('ClientDetail.urls')),
    path('', include('SorterSession.urls')),

    path('temp/', temp_data, name='temp'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
