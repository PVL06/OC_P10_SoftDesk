from django.contrib import admin
from django.contrib.auth import get_user_model

from SoftDeskAPI.models import Project


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'age',
        'can_be_contacted',
        'can_data_be_shared',
        'date_joined',
        'is_superuser',
    )
    search_fields = ('username',)
    list_per_page = 50


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'created_time'
    )
    search_fields = ('username',)
    list_per_page = 50
