from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser
from api.messages.serializers import MessageSerializer, MessageUpdateSerializer, MessageCreateSerializer
from api.models import Message
from api.permissions import IsOwner


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = permissions.IsAuthenticated

    def get_permissions(self):
        if self.action in ["destroy", "update", "partial_update"]:
            self.permission_classes = IsOwner
        elif self.action == 'list':
            self.permission_classes = IsAdminUser

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return MessageCreateSerializer
        elif self.action == "update" or self.action == "partial_update":
            return MessageUpdateSerializer
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        message = self.get_object()
        if request.user in message.conversation.participants.user:
            raise PermissionDenied('Вы не состоите в диалоге, чтобы получить данное сообщение!')
        return super().retrieve(request, *args, **kwargs)
