from rest_framework.routers import DefaultRouter

from api.conversations.views import ConversationViewSet

router = DefaultRouter()
router.register("conversations", ConversationViewSet)

urlpatterns = router.urls
