from django.contrib.auth.models import BaseUserManager
from django.core.validators import ValidationError
import re
from core.utils import phone_regex


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, first_name, last_name, phone_number, password):

        if not username:
            raise ValueError('user must have an username')

        if not email:
            raise ValueError('user must have an email')

        if not first_name:
            raise ValueError('user must have a first name')
        
        if not last_name:
            raise ValueError('user must have a last name')

        if not phone_number:
            raise ValueError('user must have a phone number')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=self.normalize_phone_number(phone_number),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, first_name, last_name, phone_number, password):
        user = self.create_user(username, email, first_name, last_name, phone_number, password)
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user

    @staticmethod
    def normalize_phone_number(phone_number, pattern=phone_regex):
        valid_phone = re.compile(pattern)
        if not valid_phone.match(phone_number):
            raise ValidationError("Phone number must be Like => +989--------- | 09---------")
        return phone_number