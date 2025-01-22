from django.contrib.auth import get_user_model

from django.contrib import admin


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