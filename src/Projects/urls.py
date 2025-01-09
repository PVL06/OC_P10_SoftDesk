from django.urls import path, include
from rest_framework import routers

from Projects.views import ProjectViewset


router = routers.SimpleRouter()
router.register('', ProjectViewset, basename='project')

urlpatterns = [
    path('', include(router.urls))
]