from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from UserAuth.serializers import UserRegistrationSerializer, UserSerializer


class UserRegistrationView(APIView):

    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewset(viewsets.ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        users = get_user_model()
        return users.objects.all()