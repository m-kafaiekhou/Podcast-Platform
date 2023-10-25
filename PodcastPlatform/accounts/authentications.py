from datetime import datetime, timedelta
from uuid import uuid4
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError, NotAcceptable, NotFound
from django.utils.translation import gettext_lazy as _

from .utils import check_cache, encode_payload, decode_token
from .exceptions import TokenExpired

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):   
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            raise NotAcceptable(_("Token not available"))

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)

        try:
            payload = decode_token(jwt_token)
        except jwt.InvalidSignatureError:
            raise ParseError(_('Invalid signature'))
        except Exception as e:
            # TODO: log e
            raise AuthenticationFailed(_('Expired Signiture'))

        if not check_cache(payload.get('jti')):
            print('not in cache'*10)
            raise NotAcceptable(_('Token not in white list'))

        user_id = payload.get('user_identifier')
        if user_id is None:
            raise NotAcceptable(_('User identifier not found in JWT'))
        print(user_id, "user_id"*10)
        user = User.objects.filter(id=user_id).first()
        if user is None:
            raise NotFound(_('User not found'))

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

        access_jwt_token = encode_payload(access_payload)

        refresh_payload = {
            'user_identifier': user_id,
            'exp': int((datetime.now() + timedelta(hours=settings.JWT_CONF['REFRESH_TOKEN_LIFETIME_HOURS'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'jti': jti,
        }

        refresh_jwt_token = encode_payload(refresh_payload)

        return access_jwt_token, refresh_jwt_token

    @classmethod 
    def get_the_token_from_header(cls, token):
        token = token.replace(settings.JWT_CONF['TOKEN_PREFIX'], '').replace(' ', '') # TODO
        return token

    @staticmethod
    def gen_jti():
        return uuid4().hex
    
    def authenticate_header(self, request):
        return settings.JWT_CONF['TOKEN_PREFIX']
