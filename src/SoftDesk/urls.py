from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_nested import routers

from SoftDeskAPI.views import ProjectViewset, IssueViewset, CommentViewset
from SoftDeskUser.views import UserViewset


user_router = routers.SimpleRouter()
user_router.register('user', UserViewset, basename='user')

project_router = routers.SimpleRouter()
project_router.register('project', ProjectViewset, basename='project')

issue_router = routers.NestedSimpleRouter(project_router, 'project', lookup='project')
issue_router.register('issue', IssueViewset, basename='issue')

comment_router = routers.NestedSimpleRouter(issue_router, 'issue', lookup='issue')
comment_router.register('comment', CommentViewset, basename='comment')

urlpatterns = [
    path('', include(user_router.urls)),
    path('', include(project_router.urls)),
    path('', include(issue_router.urls)),
    path('', include(comment_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sdapiadmin/', admin.site.urls)
]
