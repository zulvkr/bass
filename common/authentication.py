import datetime

import jwt
from app import settings
from core.models import User
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        is_ambassador = 'api/ambassador' in request.path
        is_admin = 'api/admin' in request.path

        token = request.COOKIES.get('jwt')

        if not token:
            return None

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('unauthenticated')

        # If req.path and token didn't match, throw exception

        if (is_admin and payload['scope'] != 'admin'):
            raise exceptions.AuthenticationFailed('Invalid scope!')

        # if (is_ambassador and payload['scope'] != 'ambassador'):
        #     raise exceptions.AuthenticationFailed('Invalid scope!')

        user = User.objects.get(pk=payload['user_id'])

        if user is None:
            raise exceptions.AuthenticationFailed('user not found!')

        return (user, None)

    @staticmethod
    def generate_jwt(id, scope):
        payload = {
            'user_id': id,
            'scope': scope,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
