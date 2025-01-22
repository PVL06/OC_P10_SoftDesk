from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('sdapiadmin/', admin.site.urls),
    path('', include('SoftDeskAPI.urls')),
]
