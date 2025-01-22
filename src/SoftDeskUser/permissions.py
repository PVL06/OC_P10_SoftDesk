from rest_framework import permissions


"""
An anonymous user can only access the functionality of registration and login.
A authenticated user can access the list of users and can modify or delete only their own account.
"""
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
            view.action == 'retrieve' and request.user == obj
        ]
        if any(conditions):
            return True
        return False