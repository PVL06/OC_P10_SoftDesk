from rest_framework import permissions

from SoftDeskAPI.models import Contributors


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


"""
Creation of project is accessible only for authenticated people.
The list of projects only contains those projects where the user is a contributor.
Deletion or modification of a project, issue, and comment is accessible only to their authors.
Adding an issue and a comment within a project is accessible only to authenticated users and contributors of
the project.
"""
class ProjectPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            project_id = view.kwargs.get('project_pk')
            is_contributor = Contributors.check_user_in_project(
                user=request.user,
                project_pk=project_id
            )
            conditions = [
                project_id == None,
                is_contributor
            ]
            if any(conditions):
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
