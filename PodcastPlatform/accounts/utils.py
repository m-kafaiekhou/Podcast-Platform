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
    return cached_token


def check_exp_date(exp_date):
    return datetime.now() < exp_date


def decode_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])


def encode_payload(payload):
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')