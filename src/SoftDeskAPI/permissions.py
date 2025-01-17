from rest_framework import permissions

from SoftDeskAPI.models import Contributors


class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        conditions = [
            view.action == 'create' and request.user.is_anonymous,
            view.action != 'create' and request.user.is_authenticated
        ]
        if any(conditions):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        actions = ('partial_update', 'destroy')
        conditions = [
            view.action in actions and request.user == obj,
            view.action == 'retrieve'
        ]
        if any(conditions):
            return True
        return False


class ProjectPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            is_contributor = Contributors.check_user_in_project(
                user=request.user,
                project_pk=obj.pk
            )
            author_actions = ('partial_update', 'destroy')
            conditions = [
                view.action == 'retrieve' and is_contributor,
                view.action in author_actions and request.user == obj.author
            ]
            if any(conditions):
                return True
        return False
