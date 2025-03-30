from rest_framework.routers import DefaultRouter
from .views import DriverViewSet, TruckViewSet, AssignmentViewSet

router = DefaultRouter()
router.register(r'drivers', DriverViewSet)
router.register(r'trucks', TruckViewSet)
router.register(r'assignments', AssignmentViewSet)