from rest_framework import permissions

ERROR_MESSAGE = 'You are not authorized for this action'

class UserPermissions(permissions.BasePermission):
    message = ERROR_MESSAGE

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
    message = ERROR_MESSAGE

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        actions = ('partial_update', 'destroy')
        permissions = [
            view.action in actions and request.user == obj.author,
            view.action == 'retrieve' # todo verifier si l'user est dans les contributeurs
        ]
        if any(permissions):
            return True
        return False

class ContributorPermission(permissions.BasePermission):
    message = ERROR_MESSAGE