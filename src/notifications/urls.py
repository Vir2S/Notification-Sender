from rest_framework.routers import DefaultRouter
from notifications.api import NotificationViewSet


router = DefaultRouter()
router.register("", NotificationViewSet)

urlpatterns = router.urls + []
