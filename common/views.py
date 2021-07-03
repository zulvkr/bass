from .authentication import JWTAuthentication
from core.models import User
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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

        token = JWTAuthentication.generate_jwt(user.id)
        
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
          'meassage': 'success'
        }

        return response

class UserAPIView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  def get(self, request):
    return Response(UserSerializer(request.user).data)