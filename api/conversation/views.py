from rest_framework import permissions, viewsets
from rest_framework.generics import *

from api.conversation.serializers import ConversationSerializer, AddParticipantsSerializer
from api.models import Conversation
from djoser import views


class ConversationViewSet(viewsets.ModelViewSet):
    pass


class ConversationView(ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants__user_id=self.request.user)


class AddConversationParticipantsView(CreateAPIView):
    serializer_class = AddParticipantsSerializer
    permission_classes = [permissions.IsAuthenticated]
