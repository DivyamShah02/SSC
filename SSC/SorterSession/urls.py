from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SorterViewSet


router = DefaultRouter()
router.register(r'sort', SorterViewSet, basename='sort')

urlpatterns = [
    path('', include(router.urls)),
]
