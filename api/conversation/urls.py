from rest_framework.routers import DefaultRouter

from api.conversation.views import ConversationViewSet

router = DefaultRouter()
router.register("conversation", ConversationViewSet)

urlpatterns = router.urls
