from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyInquiryViewSet, UnitClientDataViewSet


router = DefaultRouter()
router.register(r'property-inquiry', PropertyInquiryViewSet, basename='property-inquiry')
router.register(r'edit-client', UnitClientDataViewSet, basename='edit-client')

urlpatterns = [
    path('', include(router.urls)),
]
