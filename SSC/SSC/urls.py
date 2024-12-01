from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('', include('ClientDetail.urls')),
    path('', include('SorterSession.urls')),
    path('', include('Property.urls')),


    path('temp/', temp_data, name='temp'),
    path('error_page/', handle_error_page, name='error_page')
# ]
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
