from datetime import datetime, timedelta
from uuid import uuid4
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError
from .utils import check_cache

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)

        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except Exception as e:
            # TODO: log e
            raise ParseError()

        if not check_cache(payload.get('jti')):
            raise AuthenticationFailed('user not in whitelist')

        phone_number = payload.get('user_identifier')
        if phone_number is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(phone_number=phone_number).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        return user, payload

    @classmethod
    def create_jwt(cls, user_id):
        """
            Creates an access and refresh token for the user

            args:
                user_id => id of the user that sent the request
            return:
                (access token, refresh token, )
        """
        jti = cls.gen_jti()

        access_payload = {
            'user_identifier': user_id,
            'exp': int((datetime.now() + timedelta(hours=settings.JWT_CONF['TOKEN_LIFETIME_HOURS'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'jti': jti,
        }

        access_jwt_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')

        refresh_payload = {
            'user_identifier': user_id,
            'exp': int((datetime.now() + timedelta(hours=settings.JWT_CONF['REFRESH_TOKEN_LIFETIME_HOURS'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'jti': jti,
        }

        refresh_jwt_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

        return access_jwt_token, refresh_jwt_token

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')
        return token

    @staticmethod
    def gen_jti():
        return uuid4().hex
