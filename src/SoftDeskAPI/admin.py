from django.contrib import admin

from SoftDeskAPI.models import Project, Issue, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'author__username',
        'name',
        'created_time'
    )
    search_fields = ('username',)
    list_per_page = 50


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
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
