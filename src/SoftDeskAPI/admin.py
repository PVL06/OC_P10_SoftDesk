from django.contrib import admin

from SoftDeskAPI.models import Project, Issue, Comment, Contributors


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author__username',
        'name',
        'created_time'
    )
    search_fields = ('username',)
    list_per_page = 50


@admin.register(Contributors)
class ContributorAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'project_id',
        'contributor_id'
    ]
    search_fields = ('project_id',)
    list_per_page = 50


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'project',
        'name',
        'priority',
        'tag',
        'status',
        'author',
        'assigned_user',
        'created_time'
    )
    search_fields = ('username',)
    list_per_page = 50


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uuid',
        'author',
        'issue',
        'issue_link',
        'created_time'
    )
    search_fields = ('username',)
    list_per_page = 50
