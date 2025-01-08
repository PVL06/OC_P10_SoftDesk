from django.urls import path

from UserAuth.views import UserRegistrationView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register')
]