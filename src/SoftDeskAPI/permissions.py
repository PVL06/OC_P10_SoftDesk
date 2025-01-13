from rest_framework import permissions, status

class UserPermissions(permissions.BasePermission):
    message = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        if view.action == 'create' and request.user.is_anonymous:
            return True
        elif view.action != 'create' and request.user.is_authenticated:
            return True
        return False
        
    def has_object_permission(self, request, view, obj):
        actions = ('update', 'partial_update', 'destroy')
        if view.action in actions and request.user == obj:
            return True
        return False