from django.core.cache import cache
from datetime import datetime


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
    user_id = refresh_token.get('user_identifier')
    jti = refresh_token.get('jti')
    cached_token = check_cache(jti)

    if cached_token is None:
        return False

    return cached_token == user_id


def check_exp_date(exp_date):
    return datetime.now() < exp_date
