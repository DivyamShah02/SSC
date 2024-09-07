from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SorterViewSet, PropertyViewset


router = DefaultRouter()
router.register(r'sort', SorterViewSet, basename='sort')
router.register(r'view-properties', PropertyViewset, basename='view-properties')

urlpatterns = [
    path('', include(router.urls)),
]
