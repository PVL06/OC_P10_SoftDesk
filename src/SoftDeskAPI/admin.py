from django.contrib import admin

from SoftDeskAPI.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'age',
        'can_be_contacted',
        'can_data_be_shared',
        'last_login',
        'date_joined',
        'is_superuser',
    )
    search_fields = ('username',)
    list_per_page = 50

