from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.generics import *

from api.filters import UserFilter
from api.models import User
from api.serializers import UserSmallSerializer, MyConversationSerializer, ConversationSerializer


# Create your views here.
class UserSearchListView(ListAPIView):
    serializer_class = UserSmallSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = UserFilter

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class MyConversationView(ListAPIView):
    serializer_class = MyConversationSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyContactsView(ListAPIView):
    serializer_class = UserSmallSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.in_contacts


class ConversationView(CreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
