from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_nested import routers

from SoftDeskAPI.views import UserViewset, ProjectViewset, IssueViewset

user_router = routers.SimpleRouter()
user_router.register('', UserViewset, basename='user')

project_router = routers.SimpleRouter()
project_router.register(r'project', ProjectViewset, basename='project')

issue_router = routers.NestedSimpleRouter(project_router, r'project', lookup='project')
issue_router.register(r'issue', IssueViewset, basename='issue')

urlpatterns = [
    path('', include(project_router.urls)),
    path('', include(issue_router.urls)),
    path('user/', include(user_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]