from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action

from api.messages.serializers import MessageSerializer
from api.permissions import IsOwner, IsParticipant
from api.conversations.serializers import *
from api.models import Conversation


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationListSerializer
    queryset = Conversation.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(participants__user=user.pk)
        return queryset

    def get_permissions(self):
        if self.action in ["destroy", "update", "partial_update"]:
            self.permission_classes = [IsOwner]
        elif self.action == "retrieve":
            self.permission_classes = [IsParticipant]
        elif self.action == "participants":
            self.permission_classes = [IsOwner]
        elif self.action == "messages":
            self.permission_classes = [IsParticipant]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return ConversationCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return ConversationModifySerializer
        elif self.action == "destroy":
            return serializers.Serializer  # Nothing to serialize
        elif self.action == 'participants':
            return ConversationParticipantsSerializer
        elif self.action == "retrieve":
            self.permission_classes = ConversationSerializer
        elif self.action == "messages":
            self.permission_classes = MessageSerializer

        return self.serializer_class

    def participants_retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance.participants)
        return Response(serializer.data)

    def participants_create(self, request, *args, **kwargs):
        instance = self.get_object()
        self.get_serializer_context().update({'conversation', instance})
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def participants_delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(request.data)
        participants_id = serializer.validated_data()
        ConversationParticipants.objects.filter(user__in=participants_id, conversation=instance).delete()
        return Response(status.HTTP_204_NO_CONTENT)

    @action(methods=['delete', 'post', 'get'], detail=True)
    def participants(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.participants_retrieve(request, *args, **kwargs)
        elif request.method == 'POST':
            return self.participants_create(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return self.participants_delete(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def messages(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance.messages, many=True)
        return Response(serializer.data)
