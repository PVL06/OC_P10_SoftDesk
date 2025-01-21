from django_filters import rest_framework as filters

from SoftDeskAPI.models import Project, Issue, Comment


class ProjectFilter(filters.FilterSet):

    class Meta:
        model = Project
        fields = {
            'name': ['exact', 'icontains'],
            'type': ['exact']
        }


class IssueFilter(filters.FilterSet):

    class Meta:
        model = Issue
        fields = {
            'name': ['exact', 'icontains'],
            'priority': ['exact'],
            'tag': ['exact'],
            'status': ['exact']
        }


class CommentFilter(filters.FilterSet):

    class Meta:
        model = Comment
        fields = {
            'created_time': ['gt', 'lt', 'exact']
        }