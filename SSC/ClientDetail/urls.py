from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyInquiryViewSet, EditClientDataViewSet


router = DefaultRouter()
router.register(r'property-inquiry', PropertyInquiryViewSet, basename='property-inquiry')
router.register(r'edit-client', EditClientDataViewSet, basename='edit-client')

urlpatterns = [
    path('', include(router.urls)),
]
