from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.generics import ListAPIView

from api.models import Contacts, User
from api.users.filters import UserFilter
from api.users.serializers import UserSmallSerializer


class MyContactsView(ListAPIView):
    serializer_class = UserSmallSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contacts.objects.filter(user=self.request.user)


class UserSearchListView(ListAPIView):
    serializer_class = UserSmallSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = UserFilter

    def get_queryset(self):
        return User.objects.filter(is_active=True)
