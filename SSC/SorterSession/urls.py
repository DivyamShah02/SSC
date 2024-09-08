from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SorterViewSet, PropertyViewset, PropertyDetailViewset


router = DefaultRouter()
router.register(r'sort', SorterViewSet, basename='sort')
router.register(r'get-properties', PropertyViewset, basename='get-properties')
router.register(r'view-properties', PropertyDetailViewset, basename='view-properties')

urlpatterns = [
    path('', include(router.urls)),
]
