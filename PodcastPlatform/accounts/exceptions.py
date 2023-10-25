from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _

class TokenExpired(APIException):
    def __init__(self):
        detail = _("Token expired")
        super().__init__(detail, 470)

    status_code = 470
    default_detail = _('Token expired')
    default_code = 'token_expired'