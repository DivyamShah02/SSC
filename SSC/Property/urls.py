from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyDetailFormViewSet, NameAutocompleteViewSet,DocumentFormViewSet, UnitDetailFormViewSet, UnitCopyDataViewSet, PropertyCopyDataViewSet, PropertyActiveFormViewSet


router = DefaultRouter()
router.register(r'property-detail', PropertyDetailFormViewSet, basename='property-detail')
router.register(r'autocomplete-name', NameAutocompleteViewSet, basename='autocomplete-name')
router.register(r'submit-document-form', DocumentFormViewSet, basename='submit-document-form')
router.register(r'unit-details', UnitDetailFormViewSet, basename='unit-detail-form')
router.register(r'unit-copy', UnitCopyDataViewSet, basename='unit-copy')
router.register(r'property-copy', PropertyCopyDataViewSet, basename='property-copy')
router.register(r'property-publish', PropertyActiveFormViewSet, basename='property-publish')

urlpatterns = [
    path('', include(router.urls)),
]
