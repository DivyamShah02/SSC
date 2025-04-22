from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', ssc_login, name='login'),
    
    path('dashboard/', dashboard, name='dashboard'),

    path('', include('ClientDetail.urls')),
    path('', include('SorterSession.urls')),
    path('', include('Property.urls')),


    path('temp/', temp_data, name='temp'),
    path('temp_api/', temp_api, name='temp_api'),
    path('update_unit_base_price/', update_unit_base_price, name='update_unit_base_price'),
    path('update_added_by', update_added_by, name='update_added_by'),
    # path('transfer_no_of_floors/', transfer_no_of_floors, name='transfer_no_of_floors'),
    path('error_page/', handle_error_page, name='error_page')
# ]
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = not_found
handler500 = not_found_500

