from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SorterViewSet, PropertyViewset, PropertyDetailViewset, GetDistanceViewset, SelectPropertyViewSet, VisitPlanViewSet, FinalVisitPlan


router = DefaultRouter()
router.register(r'sort', SorterViewSet, basename='sort')
router.register(r'get-properties', PropertyViewset, basename='get-properties')
router.register(r'view-properties', PropertyDetailViewset, basename='view-properties')
router.register(r'get-distance', GetDistanceViewset, basename='get-distance')
router.register(r'select-property', SelectPropertyViewSet, basename='select-property')
router.register(r'visit-plan', VisitPlanViewSet, basename='visit-plan')
router.register(r'final-visit-plan', FinalVisitPlan, basename='final-visit-plan')

urlpatterns = [
    path('', include(router.urls)),
]
