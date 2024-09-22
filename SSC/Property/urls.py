from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyDetailFormViewSet


router = DefaultRouter()
router.register(r'property-detail', PropertyDetailFormViewSet, basename='property-detail')

urlpatterns = [
    path('', include(router.urls)),
]
