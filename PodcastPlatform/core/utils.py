from django.core.validators import RegexValidator


phone_regex = r'^(\+989|09)+\d{9}$'

phone_regex_validator = RegexValidator(
    regex=phone_regex, message="Invalid Phone number. Phone number must be like: +989XXXXXXXXX or 09XXXXXXXXX"
)