from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from UserAuth.serializers import UserRegistrationSerializer


class UserRegistrationView(APIView):

    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        if 'age' in serializer.errors:
            serializer.errors['age'].append('You must be over 15 years old.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

