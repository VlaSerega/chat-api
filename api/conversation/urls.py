from django.urls import re_path

from api.conversation.views import ConversationView, AddConversationParticipantsView

urlpatterns = [
    re_path(r'^conversation/', ConversationView.as_view()),
    re_path(r'^conversation/participant/add/', AddConversationParticipantsView.as_view())
]
