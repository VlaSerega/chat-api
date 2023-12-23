from rest_framework.routers import DefaultRouter

from api.messages.views import MessageViewSet

router = DefaultRouter()
router.register("conversations", MessageViewSet)

urlpatterns = router.urls
