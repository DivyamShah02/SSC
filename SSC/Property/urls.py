from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyDetailFormViewSet, DocumentFormViewSet


router = DefaultRouter()
router.register(r'property-detail', PropertyDetailFormViewSet, basename='property-detail')
router.register(r'submit-document-form', DocumentFormViewSet, basename='submit-document-form')

urlpatterns = [
    path('', include(router.urls)),
]
