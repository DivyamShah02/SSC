from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BunglowDetailFormViewSet, BunglowNameAutocompleteViewSet,BunglowDocumentFormViewSet, BunglowUnitDetailFormViewSet, BunglowUnitCopyDataViewSet, BunglowCopyDataViewSet, BunglowActiveFormViewSet


router = DefaultRouter()
router.register(r'bunglow-detail', BunglowDetailFormViewSet, basename='bunglow-detail')
router.register(r'bunglow-autocomplete-name', BunglowNameAutocompleteViewSet, basename='bunglow-autocomplete-name')
router.register(r'bunglow-submit-document-form', BunglowDocumentFormViewSet, basename='bunglow-submit-document-form')
router.register(r'bunglow-unit-details', BunglowUnitDetailFormViewSet, basename='bunglow-unit-detail-form')
router.register(r'bunglow-unit-copy', BunglowUnitCopyDataViewSet, basename='bunglow-unit-copy')
router.register(r'bunglow-copy', BunglowCopyDataViewSet, basename='bunglow-copy')
router.register(r'bunglow-publish', BunglowActiveFormViewSet, basename='bunglow-publish')

urlpatterns = [
    path('', include(router.urls)),
]
