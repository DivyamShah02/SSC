from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyDetailFormViewSet, DocumentFormViewSet, UnitDetailFormViewSet, UnitCopyDataViewSet, PropertyCopyDataViewSet


router = DefaultRouter()
router.register(r'property-detail', PropertyDetailFormViewSet, basename='property-detail')
router.register(r'submit-document-form', DocumentFormViewSet, basename='submit-document-form')
router.register(r'unit-details', UnitDetailFormViewSet, basename='unit-detail-form')
router.register(r'unit-copy', UnitCopyDataViewSet, basename='unit-copy')
router.register(r'property-copy', PropertyCopyDataViewSet, basename='property-copy')

urlpatterns = [
    path('', include(router.urls)),
]
