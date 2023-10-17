from django.core.cache import cache
from datetime import datetime
import jwt
from django.conf import settings


def cache_refresh_token(refresh_token):
    user_id = refresh_token.get('user_identifier')
    jti = refresh_token.get('jti')
    exp_date = refresh_token.get("exp")
    iat = refresh_token.get('iat')
    timeout = exp_date - iat

    cache.set(key=f'{jti}', value=f'{user_id}', timeout=timeout)


def check_cache(jti):
    c = cache.get(f'{jti}')
    if bool(c):
        return c
    return None


def delete_cache(key):
    cache.delete(f'{key}')


def validate_cached_token(refresh_token):
    jti = refresh_token.get('jti')
    cached_token = check_cache(jti)
    if cached_token and cached_token == refresh_token['user_identifier']:
        return True
    return False


def check_exp_date(exp_date):
    return datetime.now() < exp_date


def decode_token(token):
    """
    decrypts token

    args:
        token => encrypted token that was given by the user
    return:
        decrypted token
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])


def encode_payload(payload):
    """
    encrypts token

    args:
        token => encrypted token that was given by the user
    return:
        decrypted access token
    """
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')