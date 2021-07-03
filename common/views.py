from core.models import User
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Password not match!')

        data['is_ambassador'] = 0

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
          raise exceptions.AuthenticationFailed('User not found!')

        if not user.check_password(password):
          raise exceptions.AuthenticationFailed('Incorrect password.')

        return Response(UserSerializer(user).data)
