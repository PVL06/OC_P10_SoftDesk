from rest_framework import permissions
from django.shortcuts import get_object_or_404

from SoftDeskAPI.models import Contributors


class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create' and request.user.is_anonymous:
            return True
        elif view.action != 'create' and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        actions = ('partial_update', 'destroy')
        if view.action in actions and request.user == obj:
            return True
        elif view.action == 'retrieve':
            return True
        return False


class ProjectPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        is_contributor = Contributors.objects.filter(
            project_id=obj,
            contributor_id=request.user
        ).exists()
        author_actions = ('partial_update', 'destroy')

        if view.action == 'retrieve' and is_contributor:
            return True
        elif view.action in author_actions and request.user == obj.author:
            return True
        return False
