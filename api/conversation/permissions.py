from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.onwer == request.user


class IsParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.user
