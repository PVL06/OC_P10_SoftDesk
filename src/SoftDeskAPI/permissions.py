from rest_framework import permissions

from SoftDeskAPI.models import Contributors, Issue


class ProjectPermissions(permissions.BasePermission):
    """
    Creation of project is accessible only for authenticated people.
    The list of projects only contains those projects where the user is a contributor.
    Deletion or modification of a project, issue, and comment is accessible only to their authors.
    Adding an issue and a comment within a project is accessible only to authenticated users and contributors of
    the project.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            project_id = view.kwargs.get('project_pk')
            issue_id = view.kwargs.get('issue_pk')

            is_contributor = Contributors.check_user_in_project(
                user=request.user,
                project_pk=project_id
            )
            valid_project_issue = Issue.check_issue_in_project(
                project_id=project_id,
                issue_id=issue_id
            )
            conditions = [
                project_id is None,
                is_contributor and issue_id is None,
                is_contributor and issue_id and valid_project_issue
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
