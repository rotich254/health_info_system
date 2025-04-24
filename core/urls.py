from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, HealthProgramViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'programs', HealthProgramViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 